from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from ultralytics import YOLO
from config import settings

def main():
    print(f"Loading YOLO model '{settings.VEHICLE_MODEL_PATH}'...")
    model = YOLO(settings.VEHICLE_MODEL_PATH)
    ckpt_path = getattr(model, "ckpt_path", None)
    print("Model loaded successfully!")

    if ckpt_path:
        print(f"Model checkpoint path: {ckpt_path}")
    else:
        print("Couldn't determine checkpoint path, but model is ready for inference.")
    

if __name__ == "__main__":
    main()