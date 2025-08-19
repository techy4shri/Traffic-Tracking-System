# backend/app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router

app = FastAPI(title="Traffic Tracking System")

# Allow your Vercel frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"ok": True}

app.include_router(router, prefix="/api")
