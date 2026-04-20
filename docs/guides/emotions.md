# Emotion Mapping & Logic: DreamTalk Pro

DreamTalk Pro uses an advanced emotion mapping system that controls both the visual expressions and the auditory tone of the generated avatar. The system supports 30+ emotional profiles through a scalable parameter model.

## Emotional Parameters

Every emotion is defined by a set of coefficients that influence different parts of the AI pipeline.

### 1. Visual Parameters (Face/Mesh)
These coefficients influence the 3D reconstruction and animation stages:
-   **Eyebrow Position**: Vertical movement of the brows (Higher = surprised, Lower = angry/sad).
-   **Eye Openness**: The scale of the eyelid opening (Wide = excited, Narrow = suspicious/disgusted).
-   **Mouth Shape Template**: A pre-defined target shape for the lips (e.g., `smile`, `pucker`, `wide_open`).
-   **Head Motion Intensity**: Controls the frequency and amplitude of natural head sway and tilt.

### 2. Auditory Parameters (Voice)
These influence the ElevenLabs synthesis engine:
-   **Stability**: Lower values make the voice more expressive and less monotone.
-   **Similarity Boost**: Higher values ensure the voice remains consistent with the target persona.
-   **Style**: Higher values exaggerate the emotional delivery.

---

## Detailed Emotion Profiles (Examples)

The system currently supports over 30 profiles. Below are key examples:

| Emotion | Brows | Eyes | Mouth | Voice Stability | Voice Style |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Happy** | 0.2 | 0.8 | `smile` | 0.4 | 0.3 |
| **Sad** | -0.3 | 0.5 | `frown` | 0.7 | 0.0 |
| **Angry** | -0.6 | 0.9 | `tense` | 0.3 | 0.5 |
| **Surprised** | 0.7 | 1.0 | `open` | 0.35 | 0.4 |
| **Excited** | 0.5 | 0.9 | `wide_smile` | 0.3 | 0.45 |
| **Confused** | 0.3 | 0.7 | `skewed` | 0.55 | 0.1 |

---

## Intensity Scaling Logic

DreamTalk Pro supports dynamic **Emotion Intensity**. This allows for "subtle happiness" vs. "extreme joy."

### How it works:
-   Each coefficient in the `emotion_map` is multiplied by an `intensity` factor (range: 0.0 to 2.0).
-   **Visual Example**: An intensity of 0.5 on `happy` will result in a subtle smirk, while an intensity of 1.5 will create a very wide grin.
-   **Voice Example**: An intensity of 1.5 on `angry` will significantly lower stability and increase style, leading to a more volatile and intense vocal delivery.

## Implementation Details: `backend/services/emotion_mapping.py`

The logic is centralized in the `EmotionMappingService` class.

-   **`get_params(emotion, intensity)`**: Returns the final calculated coefficients for all services.
-   **Smooth Transitions**: (Future Feature) Logic to interpolate between two emotions over a specified time duration.

---

## Adding Custom Emotions

1.  Open [emotion_mapping.py](../../backend/services/emotion_mapping.py).
2.  Add a new entry to the `self.emotion_map` dictionary.
3.  Define the 5 core parameters (eyebrow, eye_open, mouth_shape, voice stability, style).
4.  The orchestrator will automatically pick up the new emotion.
5.  Update the frontend `emotions` array in `page.tsx` to display the new option.
