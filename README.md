# Project Sentinel — Gujarat CCTV Video Management & Analytics Platform (Model 5)

**Official Submission for the Gujarat Police Innovation Challenge 2026**

Project Sentinel is a state-wide, vendor-neutral **Hybrid Video Management & Analytics Platform (Model 5)** integrating ~80,000 CCTV cameras across 26 government departments into a unified command and GIS analytics ecosystem.

---

## 🌟 Key Platform Features

1. **Model 1: Centralised GIS Asset Registry**: Interactive Leaflet map displaying 50+ camera nodes across Gujarat (Ahmedabad, Gandhinagar, Surat, Vadodara, Rajkot, Dwarka, Somnath), department ownership, and real-time operational status (Online/Offline).
2. **Model 2: Unified Command Center Video Wall**: On-demand WebRTC & HLS multi-camera video stream aggregator grid without intermediate middleware storage overhead.
3. **Model 3 & 4: Distributed AI ANPR & Watchlist Matcher**: High-accuracy license plate extraction, regex normalization, and < 1ms Redis watchlist matching against VAHAN/eGujCop databases.
4. **Step 4 Live Challenge Route Tracer Engine**: Chronological vehicle trajectory reconstruction snapping target plate movement (`GJ01HK9988`) across Gujarat highways with instant real-time alert popups and audio chimes.

---

## 🚀 Quick Launch Guide

### Option 1: Full Docker Container Deployment (Recommended)

```bash
# 1. Clone & Navigate to project directory
cd "C:\Users\nidhi\Downloads\Model 5"

# 2. Build and launch all services with Docker Compose
docker-compose up --build -d

# 3. Open Command Center Dashboard in Browser:
# http://localhost
```

---

### Option 2: Standalone Local Python Execution (Zero Docker Required)

```bash
# 1. Navigate to backend directory & install dependencies
cd backend
pip install -r requirements.txt

# 2. Start FastAPI Backend & Auto-Seed 50 Gujarat Cameras
python main.py
# Backend Running at: http://localhost:8000 (API Docs at http://localhost:8000/docs)

# 3. In a new terminal, launch AI Worker Engine
cd ../ai_engine
pip install -r requirements.txt
python main.py

# 4. In a new terminal, run Frontend or open HTML5 Command Center
cd ../frontend
npm install
npm run dev
# Dashboard Running at: http://localhost:3000
```

---

## 🧪 Step 4 Challenge Demonstration

To trigger the Step 4 Live Evaluation scenario (Target Vehicle `GJ01HK9988` ANPR Detection $\rightarrow$ Instant Watchlist Match $\rightarrow$ GIS Trajectory Route Drawing):

```bash
python scripts/run_step4_demo.py
```

---

## 📁 Repository Structure

```text
Model 5/
├── docker-compose.yml              # Multi-service orchestration
├── README.md                       # Documentation & execution guide
├── backend/                        # FastAPI REST APIs, PostGIS/SQLite DB & Trajectory Engine
│   ├── main.py
│   ├── api/                        # Camera Registry, ANPR & Route Trajectory Endpoints
│   ├── db/                         # SQLAlchemy Models & 50-Camera Seed Data
│   └── services/                   # Camera Health Monitor
├── ai_engine/                      # YOLOv8 + PaddleOCR ANPR Engine & Redis Matcher
│   ├── main.py
│   ├── anpr_processor.py
│   └── watchlist_matcher.py
├── media_relay/                    # MediaMTX RTSP-to-WebRTC Video Relay
│   └── mediamtx.yml
├── frontend/                       # React Command Center (Leaflet GIS, Video Wall, Alert Toast)
│   └── src/
│       ├── components/             # GISMap, RouteTracer, VideoWall, CameraRegistry
│       └── services/api.js
└── scripts/                        # Evaluation Simulation Scripts
    ├── generate_50_streams.py
    └── run_step4_demo.py
```
