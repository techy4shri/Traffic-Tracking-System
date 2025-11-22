"""
Configuration using pydantic-settings for environment variable support.
CONFIG file: one place for thresholds, model names, and paths so I don’t hunt in code later.

Supports .env file for local development.
"""

from pathlib import Path
from typing import List
import os
import torch

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with .env support"""
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = BASE_DIR / "static" / "uploads"

    # Model paths
    VEHICLE_MODEL_PATH: str = "yolo11n.pt"

    # Inference
    # OCR settings
    DEVICE: str = "cuda" if torch.cuda.is_available() else "cpu" #i don't have nvidia so sed life no cuda for me but if you have great gpu, use it

    OCR_LANGS: List[str] = ["en"]
    CONF_VEHICLE: float = 0.35     # detector confidence for vehicles
    OCR_MIN_PLATE_LEN: int = 6
    CONF_PLATE: float = 0.35       # detector confidence for license plates
    OCR_MIN_SCORE: float = 0.55    # minimum OCR text confidence filter

    # Detection thresholds
    FRAME_SKIP: int = 2          # processes every Nth frame for videos, skipping others
    VEHICLE_CONF_THRESHOLD: float = 0.25
    OCR_CONFIDENCE_THRESHOLD: float = 0.5

    # Models (will adapt/change later, but using these for now)
    YOLO_VEHICLE_WEIGHTS: str = "yolov8n.pt"       # vehicles
    YOLO_PLATE_WEIGHTS: str = "yolov8n.pt"       # license plates

    # Video processing
    VIDEO_FRAME_STRIDE: int = 5  # Process every Nth frame

    # CORS settings
    CORS_ALLOW_ORIGINS: List[str] = ["*"]

    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 5000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Singleton instance
settings = Settings()

# Ensure directories exist (create using module-level BASE_DIR)
MODULE_BASE_DIR = Path(__file__).resolve().parent
BASE_DIR = MODULE_BASE_DIR  # Alias for backward compatibility

# create uploads dir from settings
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)

TMP_DIR = MODULE_BASE_DIR / "tmp"
TMP_DIR.mkdir(parents=True, exist_ok=True)

WEIGHTS_DIR = MODULE_BASE_DIR / "models" / "weights"
WEIGHTS_DIR.mkdir(parents=True, exist_ok=True)
