"""
Purpose: one class that loads models once and exposes clear methods:
        analyze_image(path) → counts + plate texts
        analyze_video(path) → counts/time‑series + plate texts (deduped)

Keeping vehicle detection separate from plate detection/OCR so that I can upgrade each independently (the CPU/GPU cost is taking waay long for me to figure out).
For videos, using tracking so (a) counts aren’t duplicated, and (b) you can suppress repeated OCR of the same plate.
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple
from pathlib import Path
import cv2
import numpy as np

from ultralytics import YOLO
import supervision as sv

from config import (
    DEVICE, CONF_VEHICLE, CONF_PLATE, FRAME_SKIP,
    YOLO_VEHICLE_WEIGHTS, YOLO_PLATE_WEIGHTS
)

# Choose one OCR backend; start with RapidOCR for CPU-friendliness
try:
    from rapidocr_onnxruntime import RapidOCR
    OCR_BACKEND = "rapidocr"
except Exception:
    OCR_BACKEND = None


@dataclass
class PlateRead:
    text: str
    score: float
    box: Tuple[int,int,int,int]  # x1,y1,x2,y2

@dataclass
class ImageResult:
    counts: Dict[str, int]
    plates: List[PlateRead]

@dataclass
class VideoResult:
    total_counts: Dict[str, int]
    per_class_counts: Dict[str, int]
    unique_plates: List[PlateRead]


class TrafficAnalyzer:
    def __init__(self):
        self.vehicle_model = YOLO(YOLO_VEHICLE_WEIGHTS)
        self.plate_model   = YOLO(YOLO_PLATE_WEIGHTS)
        self.vehicle_names = self.vehicle_model.model.names

        if OCR_BACKEND == "rapidocr":
            self.ocr = RapidOCR()
        else:
            self.ocr = None  # you can later plug PaddleOCR/EasyOCR here

        # tracking for videos
        self.tracker = sv.ByteTrack()

    # --- helpers ---
    def _run_yolo(self, model, image_bgr, conf) -> sv.Detections:
        res = model.predict(image_bgr, conf=conf, device=DEVICE, verbose=False)[0]
        boxes = res.boxes.xyxy.cpu().numpy() if res.boxes is not None else np.empty((0,4))
        cls   = res.boxes.cls.cpu().numpy().astype(int) if res.boxes is not None else np.empty((0,), int)
        confs = res.boxes.conf.cpu().numpy() if res.boxes is not None else np.empty((0,))
        return sv.Detections(xyxy=boxes, class_id=cls, confidence=confs)

    def _ocr_plate(self, plate_bgr) -> PlateRead | None:
        if self.ocr is None:
            return None
        # RapidOCR returns (text, score) list; keep best
        res, _ = self.ocr(plate_bgr)
        if not res:
            return None
        # Flatten + choose max score line
        best = max(res, key=lambda r: r[1])
        text = "".join(ch for ch in best[0].upper() if ch.isalnum())
        return PlateRead(text=text, score=float(best[1]), box=(0,0,plate_bgr.shape[1], plate_bgr.shape[0]))

    # --- public API ---
    def analyze_image(self, path: Path) -> ImageResult:
        im = cv2.imread(str(path))
        veh = self._run_yolo(self.vehicle_model, im, CONF_VEHICLE)

        # count per class
        counts: Dict[str,int] = {}
        for cid in veh.class_id:
            name = self.vehicle_names.get(int(cid), str(cid))
            counts[name] = counts.get(name, 0) + 1

        # plate detection on the same image
        plates: List[PlateRead] = []
        plate_det = self._run_yolo(self.plate_model, im, CONF_PLATE)
        for (x1,y1,x2,y2) in plate_det.xyxy.astype(int):
            crop = im[y1:y2, x1:x2]
            pr = self._ocr_plate(crop)
            if pr:
                pr = PlateRead(text=pr.text, score=pr.score, box=(x1,y1,x2,y2))
                plates.append(pr)

        return ImageResult(counts=counts, plates=plates)

    def analyze_video(self, path: Path) -> VideoResult:
        cap = cv2.VideoCapture(str(path))
        total_counts: Dict[str,int] = {}
        # To avoid duplicate plates, keep a set
        seen_texts: Dict[str,float] = {}
        unique_plates: List[PlateRead] = []

        # simple virtual line across middle for now
        ret, first = cap.read()
        if not ret:
            return VideoResult({}, {}, [])

        H, W = first.shape[:2]
        line = sv.LineZone(start=sv.Point(0, H//2), end=sv.Point(W, H//2))
        line_annotator = sv.LineZoneAnnotator()

        i = 0
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            if (i := i+1) % FRAME_SKIP:  # skip frames to speed up
                continue

            det = self._run_yolo(self.vehicle_model, frame, CONF_VEHICLE)
            tracked = self.tracker.update_with_detections(det)
            line.trigger(tracked)

            # count per crossing event
            for event in [line.in_count, line.out_count]:  # simple example
                pass  # you can aggregate these as needed

            # OCR on plates (you may do it only on frames where objects are near the line)
            plate_det = self._run_yolo(self.plate_model, frame, CONF_PLATE)
            for (x1,y1,x2,y2) in plate_det.xyxy.astype(int):
                crop = frame[y1:y2, x1:x2]
                pr = self._ocr_plate(crop)
                if pr and pr.text and pr.score >= 0.55:
                    # dedupe by text
                    if pr.text not in seen_texts or pr.score > seen_texts[pr.text]:
                        seen_texts[pr.text] = pr.score
                        unique_plates.append(PlateRead(pr.text, pr.score, (x1,y1,x2,y2)))

            # per-class counts each frame (coarse)
            for cid in tracked.class_id:
                name = self.vehicle_names.get(int(cid), str(cid))
                total_counts[name] = total_counts.get(name, 0) + 1

        cap.release()

        # Convert "per-frame occurrences" into an approximate count.
        # Later, replace with robust line/zone crossing counts per class.
        per_class_counts = total_counts

        return VideoResult(
            total_counts=per_class_counts,
            per_class_counts=per_class_counts,
            unique_plates=unique_plates
        )
