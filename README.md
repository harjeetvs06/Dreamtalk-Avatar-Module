# DreamTalk Pro: Advanced AI Avatar Pipeline

DreamTalk Pro is a production-level AI pipeline that transforms any static human image into a highly realistic talking 3D avatar.

## 🚀 Advanced Features

-   **Image Enhancement**: Integrated **GFPGAN** and **Real-ESRGAN** for automatic face restoration and 2x super-resolution.
-   **3D Face Reconstruction**: Uses **DECA** (Detailed Expression Capture and Animation) to generate 3D facial representations from 2D images.
-   **High-Fidelity Lip Sync**: Hybrid support for **D-ID API** and local **Wav2Lip** precision.
-   **Deep Emotion Control**: 30+ emotion mappings affecting eyebrow movement, eye openness, mouth shape, and head motion.
-   **Professional Dashboard**: A modern Next.js UI with real-time pipeline progress tracking.

## 📁 Updated Architecture

```text
avatar_module/
├── backend/
│   ├── api/             # API route definitions
│   ├── services/        # AI Services
│   │   ├── avatar_orchestrator.py # Central Controller
│   │   ├── image_processing.py    # GFPGAN/Real-ESRGAN
│   │   ├── face_reconstruction.py # DECA/3DDFA
│   │   ├── emotion_mapping.py     # 30+ Emotion Logic
│   │   └── voice_service.py       # ElevenLabs
│   └── main.py          # FastAPI Entry point
├── ai_models/           # Local weights and model code
├── frontend/            # Next.js Pro Dashboard
├── integrations/        # External API Wrappers
└── docs/                # Detailed Technical Documentation
```

## 🛠️ Installation

### 1. Requirements
-   Python 3.10+
-   CUDA-enabled GPU (Highly Recommended)
-   Node.js 18+

### 2. Environment Setup
```bash
# Install backend dependencies
pip install -r backend/requirements.txt

# Install frontend dependencies
cd frontend
npm install
```

### 3. API Configuration
Ensure your `.env` contains:
- `DID_API_KEY`
- `ELEVENLABS_API_KEY`

## 🔌 Pro API Endpoints

- `POST /generate-avatar`: Full pipeline (Enhance -> 3D -> Voice -> Video).
- `POST /enhance-image`: Standalone face restoration.
- `POST /reconstruct-face`: Standalone 3D mesh generation.
- `GET /progress/{job_id}`: Track real-time processing status.

## 🎭 Emotion Mapping
DreamTalk Pro supports advanced emotional scaling. Each emotion (e.g., `happy`, `excited`, `confused`) dynamically adjusts:
- Eyebrow position/tension
- Eye openness ratio
- Mouth shape templates
- Head motion intensity
