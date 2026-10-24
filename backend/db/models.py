import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from db.database import Base

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False) # e.g., Home Dept, RTO, Food & Civil Supplies
    contact_email = Column(String(150), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    cameras = relationship("Camera", back_populates="department")

class Camera(Base):
    __tablename__ = "cameras"

    id = Column(Integer, primary_key=True, index=True)
    camera_code = Column(String(50), unique=True, index=True, nullable=False) # e.g., CAM-AHM-001
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    vendor_name = Column(String(50), default="Hikvision") # Hikvision, Dahua, Axis, CP Plus
    rtsp_url = Column(Text, nullable=False)
    webrtc_url = Column(Text, nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    installation_address = Column(Text, nullable=False)
    district = Column(String(50), nullable=False) # e.g., Ahmedabad, Gandhinagar, Surat
    status = Column(String(20), default="ONLINE") # ONLINE, OFFLINE, DEGRADED
    fov_azimuth = Column(Integer, default=0) # 0-360 deg FOV direction
    last_ping = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    department = relationship("Department", back_populates="cameras")
    detections = relationship("ANPRDetection", back_populates="camera")

class ANPRDetection(Base):
    __tablename__ = "anpr_detections"

    id = Column(Integer, primary_key=True, index=True)
    camera_id = Column(Integer, ForeignKey("cameras.id"), nullable=False)
    detected_plate = Column(String(20), index=True, nullable=False)
    confidence = Column(Float, nullable=False, default=0.95)
    vehicle_type = Column(String(30), default="Car") # Car, Truck, Bike, Bus
    vehicle_color = Column(String(20), default="White")
    snapshot_url = Column(Text, nullable=True)
    is_watchlist_hit = Column(Boolean, default=False, index=True)
    watchlist_category = Column(String(50), nullable=True) # Stolen, Wanted, Missing, Blacklisted
    detected_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    camera = relationship("Camera", back_populates="detections")

class Watchlist(Base):
    __tablename__ = "watchlist"

    id = Column(Integer, primary_key=True, index=True)
    plate_number = Column(String(20), unique=True, index=True, nullable=False)
    reason = Column(String(200), nullable=False)
    category = Column(String(50), default="Stolen Vehicle")
    severity = Column(String(20), default="CRITICAL") # CRITICAL, HIGH, MEDIUM
    added_by_department = Column(String(100), default="Law Enforcement / Traffic Control")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
