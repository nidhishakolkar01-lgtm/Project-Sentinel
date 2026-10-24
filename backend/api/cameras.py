from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import Camera, Department
from api.auth import verify_api_key, validate_rtsp_url
from pydantic import BaseModel, Field, validator

router = APIRouter(prefix="/api/v1/cameras", tags=["Model 1: GIS Asset Registry"])

# Pydantic Schemas with Strict Input Validation
class CameraOnboardSchema(BaseModel):
    camera_code: str = Field(..., min_length=3, max_length=50, example="CAM-AHM-099")
    department_name: str = Field(..., min_length=2, max_length=100, example="Home Department / Gujarat Police")
    vendor_name: str = Field("Hikvision", max_length=50)
    rtsp_url: str = Field(..., example="rtsp://sentinel_gateway.gujarat.gov.in:8554/live/CAM-AHM-099")
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    district: str = Field(..., min_length=2, max_length=50, example="Ahmedabad")
    installation_address: str = Field(..., min_length=3, max_length=250, example="SG Highway Junction")

    @validator('camera_code')
    def sanitize_code(cls, v):
        return v.strip().upper()

class CameraResponseSchema(BaseModel):
    id: int
    camera_code: str
    department_name: str
    vendor_name: str
    rtsp_url: str
    webrtc_url: Optional[str] = None
    latitude: float
    longitude: float
    district: str
    installation_address: str
    status: str
    fov_azimuth: int

    class Config:
        from_attributes = True

@router.get("", response_model=List[CameraResponseSchema])
def list_cameras(
    district: Optional[str] = None,
    department: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Camera).join(Department)
    if district:
        query = query.filter(Camera.district.ilike(f"%{district}%"))
    if status:
        query = query.filter(Camera.status == status.upper())
    if department:
        query = query.filter(Department.name.ilike(f"%{department}%"))
    
    cameras = query.all()
    results = []
    for c in cameras:
        results.append(CameraResponseSchema(
            id=c.id,
            camera_code=c.camera_code,
            department_name=c.department.name,
            vendor_name=c.vendor_name,
            rtsp_url=c.rtsp_url,
            webrtc_url=c.webrtc_url,
            latitude=c.latitude,
            longitude=c.longitude,
            district=c.district,
            installation_address=c.installation_address,
            status=c.status,
            fov_azimuth=c.fov_azimuth
        ))
    return results

@router.post("/onboard", status_code=status.HTTP_201_CREATED)
def onboard_camera(
    payload: CameraOnboardSchema, 
    db: Session = Depends(get_db),
    authenticated: bool = Depends(verify_api_key)
):
    # Validate RTSP URL for SSRF security
    validate_rtsp_url(payload.rtsp_url)

    try:
        # Check if department exists, or create
        dept = db.query(Department).filter(Department.name == payload.department_name).first()
        if not dept:
            dept = Department(name=payload.department_name)
            db.add(dept)
            db.commit()
            db.refresh(dept)

        # Check for existing camera_code
        existing = db.query(Camera).filter(Camera.camera_code == payload.camera_code).first()
        if existing:
            raise HTTPException(status_code=400, detail=f"Camera code {payload.camera_code} already registered.")

        webrtc_url = f"http://localhost:8889/live/{payload.camera_code}"
        cam = Camera(
            camera_code=payload.camera_code,
            department_id=dept.id,
            vendor_name=payload.vendor_name,
            rtsp_url=payload.rtsp_url,
            webrtc_url=webrtc_url,
            latitude=payload.latitude,
            longitude=payload.longitude,
            district=payload.district,
            installation_address=payload.installation_address,
            status="ONLINE"
        )
        db.add(cam)
        db.commit()
        db.refresh(cam)

        return {
            "status": "SUCCESS",
            "camera_id": cam.id,
            "camera_code": cam.camera_code,
            "message": f"Camera {cam.camera_code} onboarded to GIS Asset Registry."
        }
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database commit error: {str(e)}")

@router.get("/{camera_id}", response_model=CameraResponseSchema)
def get_camera(camera_id: int, db: Session = Depends(get_db)):
    cam = db.query(Camera).filter(Camera.id == camera_id).first()
    if not cam:
        raise HTTPException(status_code=404, detail="Camera not found.")
    return CameraResponseSchema(
        id=cam.id,
        camera_code=cam.camera_code,
        department_name=cam.department.name,
        vendor_name=cam.vendor_name,
        rtsp_url=cam.rtsp_url,
        webrtc_url=cam.webrtc_url,
        latitude=cam.latitude,
        longitude=cam.longitude,
        district=cam.district,
        installation_address=cam.installation_address,
        status=cam.status,
        fov_azimuth=cam.fov_azimuth
    )
