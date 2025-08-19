"""
File handling utilities for uploads.
"""
from pathlib import Path
from typing import Literal
import shutil, uuid
from fastapi import UploadFile, HTTPException
from config import DATA_DIR

ALLOWED_IMAGE = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
ALLOWED_VIDEO = {".mp4", ".mov", ".avi", ".mkv"}

def _ext_ok(path: Path, kind: Literal["image","video"]):
    ext = path.suffix.lower()
    return ext in (ALLOWED_IMAGE if kind=="image" else ALLOWED_VIDEO)

def save_upload(file: UploadFile, kind: Literal["image","video"]) -> Path:
    suffix = Path(file.filename).suffix.lower()
    target = DATA_DIR / f"{uuid.uuid4().hex}{suffix}"
    if not _ext_ok(target, kind):
        raise HTTPException(status_code=400, detail=f"Invalid {kind} type.")
    with target.open("wb") as f:
        shutil.copyfileobj(file.file, f)
    return target
