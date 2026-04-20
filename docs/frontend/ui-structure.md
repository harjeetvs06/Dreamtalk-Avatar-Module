# Frontend & UI: DreamTalk Pro Dashboard

The DreamTalk Pro frontend is a high-performance, single-page application built with **Next.js 14** and **Tailwind CSS**. It is designed to provide a professional, dashboard-like experience for managing the complex AI avatar pipeline.

## Main View: [page.tsx](../../frontend/src/app/page.tsx)

The primary interface is split into a **Configuration Column** (left) and an **Output Preview Area** (right).

### 1. Identity Configuration
-   **Image Upload**: A drag-and-drop zone that handles `.jpg`, `.png`, and `.webp` files. It provides an immediate circular preview of the identity to be processed.
-   **Text Definition**: A robust textarea for entering speech scripts.
-   **Emotion Grid**: A quick-selection grid of buttons that map to the advanced emotional profiles (Happy, Surprised, Confused, etc.).

### 2. Pro Output Preview
-   **Dynamic Progress Tracker**: While the AI is processing, the preview area transforms into a real-time progress feed. It displays checkboxes and text for each stage of the pipeline:
    -   `Enhancing Image...`
    -   `Creating 3D Face Reconstruction...`
    -   `Generating Emotional Voice...`
    -   `Rendering Final Video...`
-   **Video Player**: Once complete, a custom HTML5 video player appears with auto-play enabled.
-   **Download Actions**: A direct link to download the high-resolution .mp4 file.

## Technical Implementation

### Asynchronous Pipeline Handling
Since generating a 3D avatar can take several seconds to a minute, the frontend uses a non-blocking architecture:
1.  **Job Submission**: The frontend sends a `multipart/form-data` request to `/generate-avatar`.
2.  **Optimistic UI**: The loading state is triggered immediately.
3.  **Simulated Stepper**: For initial UX, the dashboard cycles through the expected pipeline steps. (In production, this is synced with the backend `/progress` endpoint).
4.  **State Management**: React `useState` hooks manage the complex state of image previews, loading steps, and final URLs.

### Styling & UX
-   **Typography**: Clean sans-serif font stack for readability.
-   **Color Palette**: Minimalist zinc-based palette with **Indigo-600** as the primary action color.
-   **Animations**: Uses Tailwind's `animate-spin` for loading indicators and `animate-in` for smooth transitions between processing steps.
-   **Responsive Design**: The layout automatically shifts from a 3-column grid to a single column for tablet and mobile devices.

## Services & API Layer: `frontend/src/services/`

-   **`api.ts`**: (Future expansion) Centralized Axios or Fetch wrapper for all backend communication.
-   **`avatarService.ts`**: (Future expansion) Logic for polling the status of long-running generation jobs.
