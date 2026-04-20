# DreamTalk Pro: Advanced 3D Facial Avatar Documentation

Welcome to the technical documentation for **DreamTalk Pro**, a state-of-the-art AI pipeline for generating emotionally expressive, talking 3D avatars from static images.

## 🌟 Key Features

-   **High-Fidelity Restoration**: Integrated GFPGAN & Real-ESRGAN for professional face restoration.
-   **3D Geometry Reconstruction**: DECA-based Flame parameter extraction for natural depth and movement.
-   **Deep Emotional Intelligence**: 30+ scalable emotional profiles affecting voice and facial dynamics.
-   **Professional Pro Dashboard**: A modern Next.js interface with real-time pipeline tracking.

---

## 📚 Documentation Sections

### 1. [Architecture Overview](./architecture/overview.md)
A deep dive into the 5-stage AI pipeline and data flow architecture.

### 2. [Backend API & Services](./backend/api-services.md)
Detailed specs for FastAPI endpoints and the `AvatarOrchestrator` brain.

### 3. [AI Model Integrations](./integrations/api-integrations.md)
Technical details on GFPGAN, DECA, D-ID, and ElevenLabs integrations.

### 4. [Frontend Dashboard](./frontend/ui-structure.md)
Overview of the Pro UI, state management, and async job handling.

### 5. [Guides](./guides/)
-   [**Setup & Deployment**](./guides/setup-deployment.md): Comprehensive guide for GPU setup and installation.
-   [**Emotion Mapping & Logic**](./guides/emotions.md): Detailed parameter mapping for 30+ emotions.

---

## ⚡ Quick Start

1.  **Backend**: `cd backend && pip install -r requirements.txt && python main.py`
2.  **Frontend**: `cd frontend && npm install && npm run dev`
3.  **Config**: Ensure `.env` is populated with `DID_API_KEY` and `ELEVENLABS_API_KEY`.

---

## 🏗️ Project Structure

```text
avatar_module/
├── backend/             # FastAPI App & AI Services
├── frontend/            # Next.js Dashboard
├── integrations/        # Cloud API Wrappers
├── ai_models/           # Local GPU Model Weights
├── docs/                # Comprehensive Technical Docs
└── assets/              # Avatar and Output Storage
```
