import os
import asyncio
from typing import Optional, Dict, Any
from backend.services.image_processing import ImageProcessingService
from backend.services.face_reconstruction import FaceReconstructionService
from backend.services.emotion_mapping import EmotionMappingService
from integrations.did_api import DIDService
from configs.settings import settings

class AvatarOrchestrator:
    def __init__(self):
        self.image_service = ImageProcessingService()
        self.face_service = FaceReconstructionService()
        self.emotion_service = EmotionMappingService()
        self.did_service = DIDService()
        self.default_avatar_url = "https://create-images-results.d-id.com/Default_Avatars/v2/female_1.png"

    async def run_full_pipeline(self, image_path: str, text: str, emotion: str, intensity: float = 1.0):
        """
        Orchestrates the full AI pipeline for avatar generation.
        """
        results = {"status": "processing", "steps": []}
        
        try:
            # 1. Image Enhancement
            results["steps"].append("Enhancing Image")
            enhanced_path = await self.image_service.enhance_face(image_path)
            
            # 2. 3D Face Reconstruction
            results["steps"].append("Creating 3D Face")
            face_3d = await self.face_service.reconstruct_3d(enhanced_path)
            
            # 3. Rendering Video (D-ID or local SadTalker)
            results["steps"].append("Rendering Video")
            video_url = await self.did_service.create_talk(
                source_url=enhanced_path,  # Use enhanced image
                text=text,
                emotion=emotion
            )
            
            results.update({
                "status": "success",
                "video_url": video_url,
                "emotion_used": emotion,
                "intensity": intensity,
                "3d_face_meta": face_3d
            })
            
            return results
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "last_step": results["steps"][-1] if results["steps"] else "initialization"
            }

    async def get_progress(self, job_id: str):
        """
        Retrieves the current progress of a processing job.
        """
        # Placeholder for real-time progress tracking
        return {"job_id": job_id, "progress": "50%"}
