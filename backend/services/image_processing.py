import os
import cv2
import torch
import numpy as np
from gfpgan import GFPGANer
from realesrgan import RealESRGANer
from basicsr.archs.rrdbnet_arch import RRDBNet
from configs.settings import settings

class ImageProcessingService:
    def __init__(self, device='cuda' if torch.cuda.is_available() else 'cpu'):
        self.device = device

        # 🔥 toggle this
        self.USE_GFPGAN = False   # ⚡ set False for speed

        self.upsampler = self._init_realesrgan()

        if self.USE_GFPGAN:
            self.face_enhancer = self._init_gfpgan()
        else:
            self.face_enhancer = None

    def _init_realesrgan(self):
        model = RRDBNet(
            num_in_ch=3, num_out_ch=3,
            num_feat=64, num_block=23,
            num_grow_ch=32, scale=2
        )

        upsampler = RealESRGANer(
            scale=2,
            model_path='ai_models/realesrgan/RealESRGAN_x2plus.pth',
            model=model,

            # 🔥 SPEED SETTINGS
            tile=16,          # ⬅️ was 400 (huge slowdown)
            tile_pad=10,
            pre_pad=0,

            half=False,       # safer for CPU
            device=self.device
        )
        return upsampler

    def _init_gfpgan(self):
        return GFPGANer(
            model_path='ai_models/gfpgan/GFPGANv1.3.pth',
            upscale=2,
            arch='clean',
            channel_multiplier=2,
            bg_upsampler=self.upsampler,
            device=self.device
        )

    async def enhance_face(self, image_path: str, output_path: str = None):

        if output_path is None:
            filename = os.path.basename(image_path)
            output_path = os.path.join(
                settings.ASSETS_OUTPUTS_DIR,
                f"enhanced_{filename}"
            )

        img = cv2.imread(image_path)

        if img is None:
            raise ValueError(f"Could not read image at {image_path}")

        # 🔥 Resize input (HUGE SPEED BOOST)
        h, w = img.shape[:2]
        if max(h, w) > 512:
            scale = 512 / max(h, w)
            img = cv2.resize(img, (int(w * scale), int(h * scale)))

        # 🔥 FAST MODE (no GFPGAN)
        if not self.USE_GFPGAN:
            output, _ = self.upsampler.enhance(img, outscale=2)
            cv2.imwrite(output_path, output)
            return output_path

        # 🔥 FULL MODE (slow)
        _, _, restored_img = self.face_enhancer.enhance(
            img,
            has_aligned=False,
            only_center_face=False,
            paste_back=True
        )

        cv2.imwrite(output_path, restored_img)
        return output_path

    async def align_face(self, image_path: str):
        return image_path