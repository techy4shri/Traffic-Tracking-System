"""
Defining API surface the React App aka my frontend will hit :D (this is the 5th time I am doing this)
"""
from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from utils.file_handler import save_upload
from models.detector import TrafficAnalyzer

router = APIRouter()
analyzer = TrafficAnalyzer()  # load once

class ImageResponse(BaseModel):
    counts: dict
    plates: list

class VideoResponse(BaseModel):
    total_counts: dict
    per_class_counts: dict
    plates: list

@router.post("/analyze/image", response_model=ImageResponse)
async def analyze_image(file: UploadFile = File(...)):
    path = save_upload(file, "image")
    res = analyzer.analyze_image(path)
    return {
        "counts": res.counts,
        "plates": [{"text": p.text, "score": p.score, "box": p.box} for p in res.plates],
    }

@router.post("/analyze/video", response_model=VideoResponse)
async def analyze_video(file: UploadFile = File(...)):
    path = save_upload(file, "video")
    res = analyzer.analyze_video(path)
    return {
        "total_counts": res.total_counts,
        "per_class_counts": res.per_class_counts,
        "plates": [{"text": p.text, "score": p.score, "box": p.box} for p in res.unique_plates],
    }
