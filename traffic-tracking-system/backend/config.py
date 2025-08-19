"""
CONFIG file: one place for thresholds, model names, and paths so I don’t hunt in code later.
"""

from pathlib import Path
import torch
import os

# Define the base directory
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "static" / "uploads"
DATA_DIR.mkdir(parents=True, exist_ok=True)

#Inference
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
CONF_VEHICLE = 0.35     # detector confidence for vehicles
CONF_PLATE = 0.35       # detector confidence for license plates
OCR_MIN_SCORE = 0.55    # minimum OCR text confidence filter
FRAME_SKIP = 2          # processes every Nth frame for videos, skipping others

#Models (will adapt/change later, but using these for now)
YOLO_VEHICLE_WEIGHTS = "yolov8n.pt"       # vehicles
YOLO_PLATE_WEIGHTS   = "yolov8n.pt"       # license plates
