from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional
from backend.services.avatar_orchestrator import AvatarOrchestrator
from backend.services.image_processing import ImageProcessingService
from backend.services.face_reconstruction import FaceReconstructionService
from configs.settings import settings
import uvicorn
import os

app = FastAPI(title="DreamTalk Advanced Facial Avatar API")
orchestrator = AvatarOrchestrator()
image_service = ImageProcessingService()
face_service = FaceReconstructionService()

@app.post("/generate-avatar")
async def generate_avatar(
    text: str = Form(...),
    emotion: str = Form("neutral"),
    image: UploadFile = File(...)
):
    """
    Upgraded endpoint to handle the full AI pipeline.
    """
    # Save the uploaded file locally for processing
    os.makedirs(settings.ASSETS_AVATARS_DIR, exist_ok=True)
    temp_image_path = os.path.join(settings.ASSETS_AVATARS_DIR, image.filename)
    
    with open(temp_image_path, "wb") as buffer:
        buffer.write(await image.read())
        
    result = await orchestrator.run_full_pipeline(
        image_path=temp_image_path,
        text=text,
        emotion=emotion
    )
    
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result.get("message"))
        
    return result

@app.post("/enhance-image")
async def enhance_image(image: UploadFile = File(...)):
    """
    Independent endpoint for face restoration and super-resolution.
    """
    temp_path = os.path.join(settings.ASSETS_AVATARS_DIR, image.filename)
    with open(temp_path, "wb") as buffer:
        buffer.write(await image.read())
    
    enhanced_path = await image_service.enhance_face(temp_path)
    return {"enhanced_image_path": enhanced_path}

@app.post("/reconstruct-face")
async def reconstruct_face(image: UploadFile = File(...)):
    """
    Independent endpoint for 3D face reconstruction.
    """
    temp_path = os.path.join(settings.ASSETS_AVATARS_DIR, image.filename)
    with open(temp_path, "wb") as buffer:
        buffer.write(await image.read())
        
    reconstruction = await face_service.reconstruct_3d(temp_path)
    return reconstruction

@app.get("/progress/{job_id}")
async def get_progress(job_id: str):
    """
    Health check and progress status.
    """
    return await orchestrator.get_progress(job_id)

@app.get("/status")
async def get_status():
    """
    Health check endpoint.
    """
    return {
        "status": "online", 
        "modules": ["D-ID", "ElevenLabs", "GFPGAN", "Real-ESRGAN", "DECA"]
    }

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host=settings.HOST, port=settings.PORT, reload=True)
