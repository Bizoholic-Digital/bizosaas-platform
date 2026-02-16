from pydantic_settings import BaseSettings
from pydantic import Field
import os

class Settings(BaseSettings):
    """Global Application Settings."""
    
    # Database
    DATABASE_URL: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/bizosaas",
        env="DATABASE_URL"
    )
    
    # Temporal
    temporal_address: str = Field(
        default="localhost:7233",
        env="TEMPORAL_ADDRESS"
    )
    
    # Other URLs
    AI_AGENTS_URL: str = Field(default="http://localhost:8001", env="AI_AGENTS_URL")
    
    class Config:
        case_sensitive = False
        extra = "ignore"
        env_file = ".env"

# Initialize singleton
settings = Settings()
