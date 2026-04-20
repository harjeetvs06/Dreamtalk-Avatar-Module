# AI Model Integrations: DreamTalk Pro

DreamTalk Pro uses a hybrid of local GPU-accelerated AI models and cloud APIs to achieve the highest level of realism. This document describes each integration in detail.

---

## Local AI Pipeline (GPU)

These models are hosted locally and require NVIDIA CUDA for optimal performance.

### 1. GFPGAN (Generative Facial Prior GAN)
-   **Model**: [GFPGAN v1.3](https://github.com/TencentARC/GFPGAN)
-   **Role**: Blind Face Restoration.
-   **Integration**: Found in `backend/services/image_processing.py`.
-   **Logic**: 
    -   GFPGAN is used to restore faces in low-resolution images.
    -   It utilizes a pre-trained face GAN as a prior to hallucinate realistic facial details.
    -   It is applied in a "paste back" mode where restored faces are blended back into the original background.

### 2. Real-ESRGAN
-   **Model**: [Real-ESRGAN x2plus](https://github.com/xinntao/Real-ESRGAN)
-   **Role**: Super-resolution and background enhancement.
-   **Integration**: Used as a pre-processor for GFPGAN to upscale the entire image.
-   **Logic**: 
    -   It removes JPEG artifacts and enhances environmental details (hair, clothing, background).
    -   Configured with a `tile=400` setting to avoid OOM (Out of Memory) errors on smaller GPUs.

### 3. DECA (Detailed Expression Capture and Animation)
-   **Model**: [DECA](https://github.com/YadiraF/DECA)
-   **Role**: 3D Face Reconstruction.
-   **Integration**: Found in `backend/services/face_reconstruction.py`.
-   **Logic**: 
    -   Extracts **Flame parameters** from a single image.
    -   Separates the face into **Shape**, **Expression**, and **Pose** coefficients.
    -   This allows the system to understand the underlying geometry of the person's face for better animation alignment.

---

## Cloud API Integrations

### 1. D-ID API (Lip-Sync & Animation)
-   **Role**: High-speed, professional-grade animation rendering.
-   **Integration**: [did_api.py](../../integrations/did_api.py)
-   **Logic**: 
    -   Combines the enhanced image with synthesized audio.
    -   Applies `driver_expressions` based on the target emotion.
    -   D-ID's engine handles the complex warp and blend operations required for natural talking movement.

### 2. ElevenLabs API (Emotional Voice)
-   **Role**: State-of-the-art text-to-speech with deep emotional control.
-   **Integration**: [elevenlabs_api.py](../../integrations/elevenlabs_api.py)
-   **Logic**: 
    -   Converts text into high-fidelity speech.
    -   We programmatically adjust **Stability** (lower for more emotion), **Similarity Boost** (for consistency), and **Style** (for expressiveness) based on the target emotion label.

---

## Technical Comparison: Hybrid vs. Basic

| Feature | DreamTalk Basic | DreamTalk Pro |
| :--- | :--- | :--- |
| **Identity Prep** | Direct Upload | **GFPGAN + ESRGAN Restoration** |
| **Face Modeling** | 2D Warp | **3D Geometry (DECA)** |
| **Emotion Depth** | 5 Preset Labels | **30+ Scalable Parameters** |
| **Rendering** | Cloud API Only | **Hybrid Local Pre-processing** |
| **Output Quality** | Standard MP4 | **Super-resolution HD MP4** |
