import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Project Sentinel - Gujarat CCTV Platform"
    VERSION: str = "1.0.0"
    
    # Environment
    ENV: str = os.getenv("ENV", "development")
    
    # Security & Authentication
    API_KEY: str = os.getenv("SENTINEL_API_KEY", "sentinel_sec_key_2026_gujarat_police")
    ALLOW_ORIGINS: str = os.getenv("ALLOW_ORIGINS", "http://localhost:3000,http://localhost:8000,http://localhost:80,http://127.0.0.1:3000,http://127.0.0.1:8000")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sentinel_dev.db")
    
    # Redis
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    
    # Media Relay
    MEDIAMTX_HOST: str = os.getenv("MEDIAMTX_HOST", "localhost")
    MEDIAMTX_RTSP_PORT: int = 8554
    MEDIAMTX_WEBRTC_PORT: int = 8889
    
    # Step 4 Target Vehicle
    STEP4_TARGET_PLATE: str = os.getenv("STEP4_TARGET_PLATE", "GJ01HK9988")

    class Config:
        case_sensitive = True

settings = Settings()
