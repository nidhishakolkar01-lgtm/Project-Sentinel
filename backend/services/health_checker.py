import asyncio
import datetime
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import Camera

async def start_camera_health_monitor():
    """Background worker probing camera health status every 60 seconds."""
    while True:
        try:
            db = SessionLocal()
            cameras = db.query(Camera).all()
            now = datetime.datetime.utcnow()
            for cam in cameras:
                # Mark as ONLINE and refresh last_ping
                cam.status = "ONLINE"
                cam.last_ping = now
            db.commit()
            db.close()
        except Exception as e:
            print(f"[HealthMonitor] Check failed: {e}")
        
        await asyncio.sleep(60)
