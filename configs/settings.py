from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DID_API_KEY: str = ""
    DID_API_URL: str = "https://api.d-id.com"
    
    ELEVENLABS_API_KEY: str = ""
    ELEVENLABS_VOICE_ID: str = "21m00Tcm4TlvDq8ikWAM"
    
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    
    ASSETS_AVATARS_DIR: str = "assets/avatars"
    ASSETS_OUTPUTS_DIR: str = "assets/outputs"

    class Config:
        env_file = ".env"

settings = Settings()
