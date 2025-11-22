"""
TrafficAnalyzer: Vehicle detection + license plate OCR using YOLO and EasyOCR.
Inference-only, CPU-friendly implementation.
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple
from pathlib import Path
import re
import cv2
import numpy as np
from ultralytics import YOLO
import easyocr

from config import settings, BASE_DIR


# COCO vehicle class IDs (from YOLO COCO dataset)
VEHICLE_CLASSES = {
    2: "car",
    3: "motorcycle", 
    5: "bus",
    7: "truck"
}


@dataclass
class Box:
    """Vehicle detection bounding box"""
    bbox: Tuple[float, float, float, float]  # x1, y1, x2, y2
    label: str
    confidence: float


@dataclass
class Plate:
    """License plate detection with OCR text"""
    text: str
    bbox: Tuple[float, float, float, float]  # x1, y1, x2, y2
    confidence: float


class TrafficAnalyzer:
    """
    Main analyzer class that loads models once and provides inference methods.
    """
    
    def __init__(self):
        """Load YOLO and EasyOCR models (reused across requests)"""
        print("Loading YOLO model...")
        model_path = BASE_DIR / settings.VEHICLE_MODEL_PATH
    
        if not model_path.exists():
            print(f"Model not found at {model_path}, downloading...")
            model_path = settings.VEHICLE_MODEL_PATH.split("/")[-1]
        
        self.yolo_model = YOLO(str(model_path))
        
        print(f"Loading EasyOCR with languages: {settings.OCR_LANGS}...")
        self.ocr_reader = easyocr.Reader(settings.OCR_LANGS, gpu=False)
        
        # Indian license plate regex because I am Indian :D
        self.plate_regex = re.compile(r'[A-Z]{2}\d{1,2}[A-Z]{0,2}\d{4}')
        
        print("TrafficAnalyzer initialized successfully")
    
    def _detect_vehicles(self, image: np.ndarray) -> List[Box]:
        """
        Detect vehicles in image using YOLO.
        
        Args:
            image: BGR image as numpy array
        Returns:
            List of vehicle Box objects
        """
        results = self.yolo_model.predict(
            image,
            conf=settings.VEHICLE_CONF_THRESHOLD,
            verbose=False
        )[0]
        
        vehicles = []
        if results.boxes is not None:
            for box in results.boxes:
                class_id = int(box.cls[0])
                if class_id in VEHICLE_CLASSES:
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    confidence = float(box.conf[0])
                    label = VEHICLE_CLASSES[class_id]
                    
                    vehicles.append(Box(
                        bbox=(float(x1), float(y1), float(x2), float(y2)),
                        label=label,
                        confidence=confidence
                    ))
        
        return vehicles
    
    def _detect_plates(self, image: np.ndarray, vehicle_boxes: List[Box] = None) -> List[Plate]:
        """
        Detect and read license plates using EasyOCR.
        
        Args:
            image: BGR image as numpy array
            vehicle_boxes: Optional list of vehicle boxes to filter plates
            
        Returns:
            List of Plate objects with OCR text
        """
        # Run OCR on whole image
        ocr_results = self.ocr_reader.readtext(image)
        
        plates = []
        for bbox_coords, text, confidence in ocr_results:
            # Filter by confidence
            if confidence < settings.OCR_CONFIDENCE_THRESHOLD:
                continue
            

            clean_text = ''.join(c for c in text.upper() if c.isalnum())
            
            # Filter by minimum length and regex pattern
            if len(clean_text) < settings.OCR_MIN_PLATE_LEN:
                continue
            
            if not self.plate_regex.search(clean_text):
                continue
            
            # Convert bbox from polygon to x1,y1,x2,y2
            xs = [p[0] for p in bbox_coords]
            ys = [p[1] for p in bbox_coords]
            x1, y1, x2, y2 = min(xs), min(ys), max(xs), max(ys)
            
            # purely for extra smth but i feel like this could be useful
            if vehicle_boxes:
                if not self._box_intersects_any(
                    (x1, y1, x2, y2),
                    [v.bbox for v in vehicle_boxes]
                ):
                    continue
            
            plates.append(Plate(
                text=clean_text,
                bbox=(float(x1), float(y1), float(x2), float(y2)),
                confidence=float(confidence)
            ))
        
        return plates
    
    def _box_intersects_any(
        self,
        box: Tuple[float, float, float, float],
        boxes: List[Tuple[float, float, float, float]]
    ) -> bool:
        """Check if box intersects with any box in list"""
        x1, y1, x2, y2 = box
        
        for bx1, by1, bx2, by2 in boxes:
            # Check for intersection
            if not (x2 < bx1 or x1 > bx2 or y2 < by1 or y1 > by2):
                return True
        
        return False
    
    def analyze_image(self, image_path: Path) -> Dict:
        """
        Analyze single image for vehicles and plates.
        
        Args:
            image_path: Path to image file
            
        Returns:
            Dict with vehicle_count, vehicles list, and plates list
        """
        # Load image
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        # Detect vehicles
        vehicles = self._detect_vehicles(image)
        
        # Detect plates (optionally filter by vehicle intersection)
        plates = self._detect_plates(image, vehicle_boxes=vehicles)
        
        return {
            "vehicle_count": len(vehicles),
            "vehicles": [
                {
                    "bbox": list(v.bbox),
                    "label": v.label,
                    "confidence": v.confidence
                }
                for v in vehicles
            ],
            "plates": [
                {
                    "text": p.text,
                    "bbox": list(p.bbox),
                    "confidence": p.confidence
                }
                for p in plates
            ]
        }
    
    def analyze_video(self, video_path: Path) -> Dict:
        """
        Analyze video for vehicles and plates across sampled frames.
        
        Args:
            video_path: Path to video file
            
        Returns:
            Dict with vehicle_count (max across frames), vehicles, and plates
        """
        from utils.file_handler import iter_video_frames
        
        max_vehicle_count = 0
        all_vehicles = []
        seen_plates = {}  # text -> Plate (keep highest confidence)
        
        frame_idx = 0
        for frame in iter_video_frames(video_path, stride=settings.VIDEO_FRAME_STRIDE):
            # Detect vehicles in this frame
            vehicles = self._detect_vehicles(frame)
            
            # Track max vehicle count
            if len(vehicles) > max_vehicle_count:
                max_vehicle_count = len(vehicles)
                all_vehicles = vehicles  # Keep vehicles from frame with most detections
            
            # Detect plates in this frame
            plates = self._detect_plates(frame, vehicle_boxes=vehicles)
            
            # Deduplicate plates (keep highest confidence per text)
            for plate in plates:
                if plate.text not in seen_plates or plate.confidence > seen_plates[plate.text].confidence:
                    seen_plates[plate.text] = plate
            
            frame_idx += 1
        
        return {
            "vehicle_count": max_vehicle_count,
            "vehicles": [
                {
                    "bbox": list(v.bbox),
                    "label": v.label,
                    "confidence": v.confidence
                }
                for v in all_vehicles
            ],
            "plates": [
                {
                    "text": p.text,
                    "bbox": list(p.bbox),
                    "confidence": p.confidence
                }
                for p in seen_plates.values()
            ]
        }
