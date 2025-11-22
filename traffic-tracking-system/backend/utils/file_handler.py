"""
File handling utilities for uploads and video processing.File handling utilities for uploads.
"""
from pathlib import Path
from typing import Literal, Iterator
import shutil
import uuid
from fastapi import UploadFile, HTTPException

from config import DATA_DIR, TMP_DIR

import cv2
import numpy as np

ALLOWED_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff"}
ALLOWED_VIDEO_EXTS = {".mp4", ".mov", ".avi", ".mkv", ".m4v", ".webm"}

def _ext_ok(path: Path, kind: Literal["image", "video"]) -> bool:
    ext = path.suffix.lower()
    return ext in (ALLOWED_IMAGE_EXTS if kind == "image" else ALLOWED_VIDEO_EXTS)

def is_image(filename: str) -> bool:
    """Check if filename has an image extension"""
    return Path(filename).suffix.lower() in ALLOWED_IMAGE_EXTS

def is_video(filename: str) -> bool:
    """Check if filename has a video extension"""
    return Path(filename).suffix.lower() in ALLOWED_VIDEO_EXTS

async def save_upload(file: UploadFile) -> Path:
    """
    Save uploaded file to tmp directory with UUID filename.
    Validates extension and raises HTTPException on invalid type.

    Args:
        file: FastAPI UploadFile from multipart form
    Returns:
        Path to saved file
    Raises:
        HTTPException: If file extension is not allowed
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    suffix = Path(file.filename).suffix.lower()

    # Validate extension
    if suffix not in (ALLOWED_IMAGE_EXTS | ALLOWED_VIDEO_EXTS):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type '{suffix}'. Allowed: images ({', '.join(sorted(ALLOWED_IMAGE_EXTS))}) "
                   f"or videos ({', '.join(sorted(ALLOWED_VIDEO_EXTS))})"
        )

    # Generate unique filename
    unique_name = f"{uuid.uuid4().hex}{suffix}"
    target_path = TMP_DIR / unique_name

    # Save file
    try:
        with target_path.open("wb") as f:
            shutil.copyfileobj(file.file, f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    return target_path

def iter_video_frames(video_path: Path, stride: int = 1) -> Iterator[np.ndarray]:
    """
    Iterate over video frames with optional stride (skip frames).

    Args:
        video_path: Path to video file
        stride: Process every Nth frame (default 1 = all frames)

    Yields:
        Frame as numpy array (BGR format)

    Raises:
        HTTPException: If video cannot be opened
    """
    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        raise HTTPException(status_code=400, detail="Could not open video file")

    frame_idx = 0
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Only yield frames matching stride
            if frame_idx % stride == 0:
                yield frame

            frame_idx += 1
    finally:
        cap.release()
