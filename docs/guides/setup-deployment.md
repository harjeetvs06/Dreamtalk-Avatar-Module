# Setup & Deployment Guide: DreamTalk Pro

This guide covers the technical requirements and installation steps for DreamTalk Pro, a high-performance AI avatar pipeline.

---

## Hardware Prerequisites

DreamTalk Pro is optimized for local GPU inference.

-   **GPU**: NVIDIA RTX 3060 or higher (8GB+ VRAM recommended).
-   **CUDA**: Version 11.8 or 12.1.
-   **Memory**: 16GB+ RAM.
-   **Storage**: 50GB+ free SSD space (for models and assets).

---

## 1. Environment Configuration

### Clone the Repository
```bash
git clone https://github.com/your-org/dreamtalk-facial-model.git
cd dreamtalk-facial-model
```

### Configure API Keys
Create a `.env` file in the root directory:
```env
DID_API_KEY=your_did_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM
PORT=8000
HOST=0.0.0.0
```

---

## 2. Backend Installation (Python)

### Create Virtual Environment
```bash
cd backend
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

### Install Dependencies
```bash
# Install PyTorch with CUDA support (example for CUDA 11.8)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install other requirements
pip install -r requirements.txt
```

---

## 3. Download AI Model Weights

The system requires pre-trained weights for the local pipeline. Download these and place them in the `ai_models/` folder.

| Model | Path | Source |
| :--- | :--- | :--- |
| **GFPGAN** | `ai_models/gfpgan/GFPGANv1.3.pth` | [GFPGAN Releases](https://github.com/TencentARC/GFPGAN/releases) |
| **Real-ESRGAN** | `ai_models/realesrgan/RealESRGAN_x2plus.pth` | [Real-ESRGAN Releases](https://github.com/xinntao/Real-ESRGAN/releases) |
| **DECA** | `ai_models/deca/deca_model.pth` | [DECA Weights](https://github.com/YadiraF/DECA) |

---

## 4. Frontend Installation (Next.js)

### Install Node Dependencies
```bash
cd frontend
npm install
```

### Development Mode
```bash
npm run dev
```

---

## 5. Deployment Options

### Docker Deployment (Recommended)
DreamTalk Pro is best deployed via Docker with NVIDIA Container Toolkit.

```bash
docker-compose up --build
```
Ensure your `docker-compose.yml` includes:
-   `deploy.resources.reservations.devices.driver: nvidia`
-   Mapped volumes for `ai_models/` and `assets/`.

### Production Server
-   Use **Gunicorn** with **Uvicorn** workers for the FastAPI backend.
-   Use **Nginx** as a reverse proxy for the frontend and static assets.
-   Implement a background worker (e.g., **Celery** or **RQ**) for jobs exceeding 60 seconds.

---

## Troubleshooting

### CUDA Errors (Out of Memory)
-   Increase the `tile` size in `ImageProcessingService` (e.g., from 400 to 200).
-   Use `half=True` (FP16) in the model initialization settings.

### API Failures
-   Check your D-ID or ElevenLabs credit balance.
-   Ensure your server has outbound internet access to `api.d-id.com` and `api.elevenlabs.io`.
