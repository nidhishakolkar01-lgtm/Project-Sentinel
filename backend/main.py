import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from config import settings
from db.seed_data import init_db
from api import cameras, analytics, tracking, websockets
from services.health_checker import start_camera_health_monitor

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Initialize DB and Seed 50 Cameras & Step 4 Watchlist Data
    print("[Sentinel Backend] Initializing Database & Seed Data...")
    init_db()
    
    # 2. Start Background Camera Health Monitor Task
    health_task = asyncio.create_task(start_camera_health_monitor())
    
    yield
    
    health_task.cancel()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Project Sentinel — Enterprise-Grade Distributed Video Management & Real-Time GIS Analytics Platform",
    lifespan=lifespan
)

# Parse configured CORS origins securely
origins = [origin.strip() for origin in settings.ALLOW_ORIGINS.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins else ["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(cameras.router)
app.include_router(analytics.router)
app.include_router(tracking.router)
app.include_router(websockets.router)

# Custom Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"[ERROR] Unhandled Exception: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"status": "ERROR", "detail": "An internal server error occurred. Please check system logs."}
    )

@app.get("/")
def root():
    return {
        "status": "ONLINE",
        "system": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENV,
        "model_architecture": "Model 5 (Hybrid Architecture: Model 1 Registry + Model 3 Middleware + Model 2 Unified Viewer)",
        "step4_challenge_status": "READY",
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
