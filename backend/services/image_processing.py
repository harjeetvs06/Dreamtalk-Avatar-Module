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
        self.upsampler = self._init_realesrgan()
        self.face_enhancer = self._init_gfpgan()

    def _init_realesrgan(self):
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2)
        upsampler = RealESRGANer(
            scale=2,
            model_path='ai_models/realesrgan/RealESRGAN_x2plus.pth',
            model=model,
            tile=400,
            tile_pad=10,
            pre_pad=0,
            half=True if self.device == 'cuda' else False,
            device=self.device
        )
        return upsampler

    def _init_gfpgan(self):
        face_enhancer = GFPGANer(
            model_path='ai_models/gfpgan/GFPGANv1.3.pth',
            upscale=2,
            arch='clean',
            channel_multiplier=2,
            bg_upsampler=self.upsampler,
            device=self.device
        )
        return face_enhancer

    async def enhance_face(self, image_path: str, output_path: str = None):
        """
        Enhances the input image using GFPGAN for faces and Real-ESRGAN for background.
        """
        if output_path is None:
            filename = os.path.basename(image_path)
            output_path = os.path.join(settings.ASSETS_OUTPUTS_DIR, f"enhanced_{filename}")

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not read image at {image_path}")

        # Enhance faces and background
        _, _, restored_img = self.face_enhancer.enhance(
            img,
            has_aligned=False,
            only_center_face=False,
            paste_back=True
        )

        cv2.imwrite(output_path, restored_img)
        return output_path

    async def align_face(self, image_path: str):
        """
        Detects and aligns face for 3D reconstruction.
        Placeholder for InsightFace alignment logic.
        """
        # Implementation would use InsightFace or Mediapipe
        return image_path
