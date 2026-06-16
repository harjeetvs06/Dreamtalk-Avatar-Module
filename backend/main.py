from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
from backend.services.avatar_orchestrator import AvatarOrchestrator
from backend.services.image_processing import ImageProcessingService
from backend.services.face_reconstruction import FaceReconstructionService
from configs.settings import settings
import uvicorn
import os

app = FastAPI(title="DreamTalk Advanced Facial Avatar API")

# Enable CORS so frontend can call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure avatar assets folder exists
os.makedirs(settings.ASSETS_AVATARS_DIR, exist_ok=True)

# Serve avatar/output images publicly
app.mount(
    "/avatars",
    StaticFiles(directory=settings.ASSETS_AVATARS_DIR),
    name="avatars"
)
os.makedirs(settings.ASSETS_OUTPUTS_DIR, exist_ok=True)

app.mount(
    "/outputs",
    StaticFiles(directory=settings.ASSETS_OUTPUTS_DIR),
    name="outputs"
)
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
    Full avatar pipeline endpoint.
    Uploads an image, processes it, and returns avatar output.
    """
    try:
        os.makedirs(settings.ASSETS_AVATARS_DIR, exist_ok=True)

        temp_image_path = os.path.join(
            settings.ASSETS_AVATARS_DIR,
            image.filename
        )

        with open(temp_image_path, "wb") as buffer:
            buffer.write(await image.read())

        result = await orchestrator.run_full_pipeline(
            image_path=temp_image_path,
            text=text,
            emotion=emotion
        )

        if result.get("status") == "error":
            raise HTTPException(
                status_code=500,
                detail=result.get("message")
            )

        return result

    except HTTPException:
        raise

    except Exception as e:
        import traceback
        print("GENERATE AVATAR ERROR:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/enhance-image")
async def enhance_image(image: UploadFile = File(...)):
    """
    Independent endpoint for face restoration and super-resolution.
    """
    try:
        os.makedirs(settings.ASSETS_AVATARS_DIR, exist_ok=True)

        temp_path = os.path.join(
            settings.ASSETS_AVATARS_DIR,
            image.filename
        )

        with open(temp_path, "wb") as buffer:
            buffer.write(await image.read())

        enhanced_path = await image_service.enhance_face(temp_path)

        filename = os.path.basename(enhanced_path)

        return {
            "status": "success",
            "enhanced_image_path": enhanced_path,
            "enhanced_image_url": f"/avatars/{filename}"
        }

    except Exception as e:
        import traceback
        print("ENHANCE IMAGE ERROR:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/reconstruct-face")
async def reconstruct_face(image: UploadFile = File(...)):
    """
    Independent endpoint for 3D face reconstruction.
    """
    try:
        os.makedirs(settings.ASSETS_AVATARS_DIR, exist_ok=True)

        temp_path = os.path.join(
            settings.ASSETS_AVATARS_DIR,
            image.filename
        )

        with open(temp_path, "wb") as buffer:
            buffer.write(await image.read())

        reconstruction = await face_service.reconstruct_3d(temp_path)

        return {
            "status": "success",
            "reconstruction": reconstruction
        }

    except Exception as e:
        import traceback
        print("RECONSTRUCT FACE ERROR:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/progress/{job_id}")
async def get_progress(job_id: str):
    """
    Progress status endpoint.
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
    uvicorn.run(
        "backend.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )