# Backend API & Services: DreamTalk Pro

The backend of DreamTalk Pro is built on **FastAPI**, designed for high-performance, asynchronous processing of complex AI workloads. It manages a sophisticated pipeline involving multiple local and cloud-based AI models.

## Entry Point: `main.py`

The main application handles routing, request validation, and multi-part file uploads.

### Core Endpoints

#### `POST /generate-avatar`
-   **Description**: The primary entry point for generating a full-motion avatar. It orchestrates the entire pipeline from image enhancement to video rendering.
-   **Request (Form-Data)**:
    -   `text`: The content the avatar should speak.
    -   `emotion`: The target emotional state (e.g., `happy`, `surprised`).
    -   `image`: The source photo (UploadFile).
-   **Response**: 
    -   `video_url`: Publicly accessible link to the generated .mp4.
    -   `3d_face_meta`: Meta-information from the reconstruction stage.
    -   `emotion_used`: The final emotion profile applied.

#### `POST /enhance-image`
-   **Description**: Standalone access to the **GFPGAN/Real-ESRGAN** pipeline. Useful for UI-only enhancements.
-   **Response**: `enhanced_image_path`: Path to the upscaled and restored image.

#### `POST /reconstruct-face`
-   **Description**: Standalone access to the **DECA** reconstruction engine.
-   **Response**: Returns 3D mesh parameters and facial landmark data.

#### `GET /progress/{job_id}`
-   **Description**: Polls the current state of a long-running generation task.
-   **States**: `initializing`, `enhancing`, `reconstructing`, `synthesizing`, `rendering`, `complete`, `failed`.

---

## Orchestration Logic: `AvatarOrchestrator`

The `AvatarOrchestrator` (found in [avatar_orchestrator.py](../../backend/services/avatar_orchestrator.py)) is the "brain" of the backend.

### Pipeline Management
It manages the execution order of services:
1.  **ImageService**: Enhances the raw input using blind face restoration.
2.  **FaceService**: Extracts 3D geometry and landmarks from the enhanced image.
3.  **VoiceService**: Synthesizes emotional speech using ElevenLabs.
4.  **AnimationService**: Combines all assets to render the final video via D-ID or local drivers.

### Error Resilience
-   **Retry Mechanisms**: Automatic retries for cloud API failures.
-   **Graceful Degradation**: If 3D reconstruction fails, the system falls back to 2D-only animation.
-   **State Tracking**: Each step is logged and trackable via the `/progress` endpoint.

---

## Internal AI Services

### `ImageProcessingService`
-   **Logic**: Uses a two-pass approach. Pass 1 enhances the background with Real-ESRGAN. Pass 2 restores facial details using GFPGAN and pastes them back.
-   **Device**: Configurable to run on `cpu` or `cuda`.

### `FaceReconstructionService`
-   **Logic**: High-level wrapper for DECA. It extracts the Flame parameters from the 2D image, allowing the avatar to move its head and change expressions more naturally.

### `EmotionMappingService`
-   **Logic**: Translates human-readable emotion labels into a set of 15+ numerical coefficients for voice (ElevenLabs) and 30+ coefficients for facial movement (D-ID/DECA).
