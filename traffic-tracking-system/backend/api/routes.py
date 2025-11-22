"""
API routes for traffic analysis endpoints.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List

from utils.file_handler import save_upload
from models.detector import TrafficAnalyzer


# Initialize router
router = APIRouter()

# Load analyzer once (singleton)
print("Initializing TrafficAnalyzer...")
analyzer = TrafficAnalyzer()


# Response models
class VehicleDetection(BaseModel):
    """Single vehicle detection"""
    bbox: List[float]  # [x1, y1, x2, y2]
    label: str
    confidence: float


class PlateDetection(BaseModel):
    """Single plate OCR result"""
    text: str
    bbox: List[float]  # [x1, y1, x2, y2]
    confidence: float


class AnalysisResponse(BaseModel):
    """Response schema for both image and video analysis"""
    vehicle_count: int
    vehicles: List[VehicleDetection]
    plates: List[PlateDetection]


@router.get("/ping")
async def ping():
    """Health check endpoint"""
    return {"status": "ok"}


@router.post("/analyze/image", response_model=AnalysisResponse)
async def analyze_image(file: UploadFile = File(...)):
    """
    Analyze uploaded image for vehicles and license plates.
    
    Args:
        file: Image file (jpg, png, etc.)
        
    Returns:
        AnalysisResponse with vehicle count, detections, and plates
    """
    try:
        # Save upload
        file_path = await save_upload(file)
        
        # Run analysis
        result = analyzer.analyze_image(file_path)
        
        # Clean up file
        file_path.unlink(missing_ok=True)
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/analyze/video", response_model=AnalysisResponse)
async def analyze_video(file: UploadFile = File(...)):
    """
    Analyze uploaded video for vehicles and license plates.
    Samples frames and returns aggregate results.
    
    Args:
        file: Video file (mp4, avi, etc.)
        
    Returns:
        AnalysisResponse with max vehicle count, detections, and unique plates
    """
    try:
        # Save upload
        file_path = await save_upload(file)
        
        # Run analysis
        result = analyzer.analyze_video(file_path)
        
        # Clean up file
        file_path.unlink(missing_ok=True)
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
