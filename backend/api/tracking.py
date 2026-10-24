from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import ANPRDetection, Camera
from pydantic import BaseModel
import datetime
import math

router = APIRouter(prefix="/api/v1/tracking", tags=["Step 4 Challenge: Vehicle Route Trajectory Engine"])

class TrajectoryPointSchema(BaseModel):
    sequence: int
    camera_id: int
    camera_code: str
    location_name: str
    district: str
    latitude: float
    longitude: float
    detected_plate: str
    timestamp: datetime.datetime
    confidence: float
    snapshot_url: Optional[str] = None

class RouteResponseSchema(BaseModel):
    target_plate: str
    total_checkpoints: int
    total_distance_km: float
    first_seen: datetime.datetime
    last_seen: datetime.datetime
    trajectory: List[TrajectoryPointSchema]

def calculate_distance(lat1, lon1, lat2, lon2):
    # Haversine formula to compute geodesic distance between GPS checkpoints
    R = 6371.0 # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@router.get("/route", response_model=RouteResponseSchema)
def get_vehicle_route(
    plate: str = Query(..., description="Target Vehicle License Plate Number (e.g. GJ01HK9988)"),
    db: Session = Depends(get_db)
):
    plate_clean = plate.upper().replace("-", "").replace(" ", "")
    
    detections = (
        db.query(ANPRDetection)
        .join(Camera)
        .filter(ANPRDetection.detected_plate == plate_clean)
        .order_by(ANPRDetection.detected_at.asc())
        .all()
    )

    if not detections:
        raise HTTPException(
            status_code=404, 
            detail=f"No detections found for vehicle plate '{plate_clean}'."
        )

    trajectory = []
    total_dist = 0.0

    for idx, d in enumerate(detections):
        point = TrajectoryPointSchema(
            sequence=idx + 1,
            camera_id=d.camera.id,
            camera_code=d.camera.camera_code,
            location_name=d.camera.installation_address,
            district=d.camera.district,
            latitude=d.camera.latitude,
            longitude=d.camera.longitude,
            detected_plate=d.detected_plate,
            timestamp=d.detected_at,
            confidence=d.confidence,
            snapshot_url=d.snapshot_url
        )
        trajectory.append(point)

        if idx > 0:
            prev_point = trajectory[idx - 1]
            total_dist += calculate_distance(
                prev_point.latitude, prev_point.longitude,
                point.latitude, point.longitude
            )

    return RouteResponseSchema(
        target_plate=plate_clean,
        total_checkpoints=len(trajectory),
        total_distance_km=round(total_dist, 2),
        first_seen=trajectory[0].timestamp,
        last_seen=trajectory[-1].timestamp,
        trajectory=trajectory
    )
