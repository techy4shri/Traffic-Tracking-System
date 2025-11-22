"""
FastAPI application for Traffic Tracking System backend.
Inference-only vehicle detection and license plate recognition.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from api.routes import router


# Create FastAPI app
app = FastAPI(
    title="Traffic Tracking System API",
    description="Vehicle detection and license plate recognition using YOLO + EasyOCR",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint with API info"""
    return {
        "message": "Traffic Tracking System API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/ping"
    }


# Mount API router
app.include_router(router, prefix="/api", tags=["analysis"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
