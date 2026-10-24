from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import ANPRDetection, Camera, Watchlist
from api.auth import verify_api_key
from pydantic import BaseModel, Field, validator
import datetime

router = APIRouter(prefix="/api/v1/analytics", tags=["Model 2 & 4: ANPR & AI Analytics"])

class DetectionSchema(BaseModel):
    id: int
    camera_code: str
    location_name: str
    district: str
    detected_plate: str
    confidence: float
    vehicle_type: str
    vehicle_color: str
    is_watchlist_hit: bool
    watchlist_category: Optional[str] = None
    detected_at: datetime.datetime

    class Config:
        from_attributes = True

class WatchlistAddSchema(BaseModel):
    plate_number: str = Field(..., min_length=4, max_length=20, example="GJ01HK9988")
    reason: str = Field(..., min_length=3, max_length=200, example="Stolen SUV - FIR #402/2026")
    category: str = Field("Stolen Vehicle", max_length=50)
    severity: str = Field("CRITICAL", max_length=20)

    @validator('plate_number')
    def clean_plate(cls, v):
        return v.upper().replace("-", "").replace(" ", "").strip()

@router.get("/detections", response_model=List[DetectionSchema])
def list_detections(
    plate: Optional[str] = None,
    watchlist_hits_only: bool = False,
    limit: int = Query(default=50, le=200),
    db: Session = Depends(get_db)
):
    query = db.query(ANPRDetection).join(Camera)
    if plate:
        clean_p = plate.upper().replace("-", "").replace(" ", "")
        query = query.filter(ANPRDetection.detected_plate.ilike(f"%{clean_p}%"))
    if watchlist_hits_only:
        query = query.filter(ANPRDetection.is_watchlist_hit == True)

    detections = query.order_by(ANPRDetection.detected_at.desc()).limit(limit).all()
    
    results = []
    for d in detections:
        results.append(DetectionSchema(
            id=d.id,
            camera_code=d.camera.camera_code,
            location_name=d.camera.installation_address,
            district=d.camera.district,
            detected_plate=d.detected_plate,
            confidence=d.confidence,
            vehicle_type=d.vehicle_type,
            vehicle_color=d.vehicle_color,
            is_watchlist_hit=d.is_watchlist_hit,
            watchlist_category=d.watchlist_category,
            detected_at=d.detected_at
        ))
    return results

@router.post("/watchlist", status_code=status.HTTP_201_CREATED)
def add_to_watchlist(
    payload: WatchlistAddSchema, 
    db: Session = Depends(get_db),
    authenticated: bool = Depends(verify_api_key)
):
    try:
        existing = db.query(Watchlist).filter(Watchlist.plate_number == payload.plate_number).first()
        if existing:
            existing.reason = payload.reason
            existing.category = payload.category
            existing.severity = payload.severity
            db.commit()
            return {"status": "UPDATED", "plate_number": payload.plate_number, "message": "Watchlist record updated."}

        w = Watchlist(
            plate_number=payload.plate_number,
            reason=payload.reason,
            category=payload.category,
            severity=payload.severity
        )
        db.add(w)
        db.commit()
        return {"status": "CREATED", "plate_number": payload.plate_number, "message": "Vehicle added to live watchlist."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database transaction error: {str(e)}")

@router.get("/watchlist")
def get_watchlist(db: Session = Depends(get_db)):
    items = db.query(Watchlist).all()
    return items
