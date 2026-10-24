# Project Sentinel — Intelligent CCTV Video Management & GIS Analytics Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.4-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Leaflet](https://img.shields.io/badge/Leaflet-GIS-199900?style=for-the-badge&logo=leaflet&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-7.0-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-PostGIS-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)

**An enterprise-grade, distributed Video Management System (VMS) and AI-driven spatial intelligence platform designed for large-scale camera asset management, sub-second WebRTC video streaming, real-time license plate recognition (ANPR), and automated vehicle route trajectory reconstruction.**

[Key Features](#-key-features) • [Architecture](#-system-architecture) • [Quick Start](#-quick-start-guide) • [API Reference](#-api-documentation) • [Demo Walkthrough](#-interactive-evaluation--demo) • [Security](#-security--defensive-design)

</div>

---

## 📌 Overview

**Project Sentinel** solves the critical operational challenges of managing large, distributed surveillance networks spanning thousands of multi-vendor CCTV cameras across diverse departments and geographical regions. 

Surveillance networks are often fragmented across disparate vendor ecosystems (Hikvision, Dahua, Axis, CP Plus) with isolated viewing software, proprietary protocols, and high bandwidth costs. Project Sentinel establishes a unified, vendor-neutral command center integrating:

1. **Centralized GIS Asset Registry**: Interactive geospatial asset mapping displaying camera coordinates, installation sites, ownership departments, and live health statuses.
2. **Unified Command Center Video Wall**: Zero-latency RTSP-to-WebRTC stream relaying providing on-demand $2\times2$ and $3\times3$ live grid views without intermediate disk transcoding.
3. **Distributed AI ANPR Engine**: Automated License Plate Recognition utilizing YOLOv8 vehicle detection, PaddleOCR text extraction, and positional regex normalizers tailored for standard license plate formats.
4. **Sub-Millisecond Watchlist Matcher**: Ultra-fast Redis in-memory cache cross-referencing incoming detections against hot watchlists (stolen vehicles, wanted alerts) in under 1ms.
5. **Geodesic Vehicle Route Trajectory Engine**: Chronological trajectory reconstruction connecting sequential camera detections and computing total distance traversed using the **Haversine formula**.
6. **Real-Time Operator Alerting**: Full-duplex WebSocket push notifications with instant UI HUD popups and in-browser emergency audio chimes ($880\text{ Hz}$) generated via the Web Audio API.

---

## 🌟 Key Features

| Capability | Technical Implementation | Operational Benefit |
| :--- | :--- | :--- |
| **Vendor-Agnostic GIS Registry** | React + Leaflet + PostGIS / SQLite WAL | Single pane of glass for camera locations, status pings, and departmental tags across vendors. |
| **Sub-300ms Live Video Wall** | MediaMTX RTSP $\rightarrow$ WebRTC Gateway | Zero-install, browser-native live video feeds eliminating client plugins and heavy transcoder servers. |
| **AI Plate Normalization** | YOLOv8 + PaddleOCR + Regex Heuristics | Robust handling of noisy OCR outputs (e.g., $O \leftrightarrow 0, I \leftrightarrow 1, Z \leftrightarrow 2$) for Indian and international plates. |
| **Real-Time Watchlist Engine** | Redis In-Memory Hash Pool (`< 1ms`) | Instant detection-to-alert matching with automated fallback to in-memory store if Redis is unavailable. |
| **Geodesic Trajectory Reconstruction** | Haversine Great-Circle Math + Leaflet Polyline | Snaps chronological checkpoints into a continuous visual route path with exact travel distances in kilometers. |
| **Operator Audio-Visual HUD** | WebSockets + Web Audio API ($880\text{ Hz}$) | Immediate acoustic alert and map focus for operators when high-severity targets are detected. |
| **Defensive Resiliency** | Multi-Tier Offline Fallbacks | Built-in mock data generators and cache fallbacks guarantee the dashboard remains fully operational during presentations or network outages. |

---

## 🏛️ System Architecture

```text
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                   Web Command Center (React 18 + Leaflet)               │
 │  ┌──────────────────────┬──────────────────────┬─────────────────────┐  │
 │  │   GIS Map Display    │   Video Wall Grid    │ Route Tracer Engine │  │
 │  └──────────▲───────────┴──────────▲───────────┴──────────▲──────────┘  │
 └─────────────┼──────────────────────┼──────────────────────┼─────────────┘
               │ WebSockets           │ WebRTC (Sub-300ms)   │ REST / JSON
               │ (/ws/alerts)         │                      │
 ┌─────────────┴──────────────────────┴──────────────────────┴─────────────┐
 │                         MediaMTX Video Relay Engine                     │
 │  RTSP TCP (Port 8554) ──► Low-Latency WebRTC / HLS Gateway (Port 8889)   │
 └────────────────────────────────────▲────────────────────────────────────┘
                                      │ Ingest
 ┌────────────────────────────────────┴────────────────────────────────────┐
 │                  FastAPI Application Gateway & Trajectory Core          │
 │  ┌───────────────────────┬──────────────────────┬────────────────────┐  │
 │  │  Camera GIS Registry  │  Trajectory Engine   │ Watchlist / ANPR   │  │
 │  │  (/api/v1/cameras)    │  (/api/v1/tracking)  │ (/api/v1/analytics)│  │
 │  └──────────┬────────────┴──────────┬───────────┴──────────┬─────────┘  │
 └─────────────┼───────────────────────┼──────────────────────┼────────────┘
               │ Read/Write            │ Geodesic Query       │ < 1ms Match
               ▼                       ▼                      ▼
 ┌───────────────────────────┐ ┌───────────────────┐ ┌─────────────────────┐
 │    PostGIS / SQLite DB    │ │  Camera Health    │ │ Redis In-Memory     │
 │  - 50 Seeded Cameras      │ │  Background Task  │ │ Watchlist Cache     │
 │  - 26 Departments         │ │  (60s Prober)     │ │ (Hash Lookup)       │
 └───────────────────────────┘ └───────────────────┘ └─────────────────────┘
                                                              ▲
                                                              │ Hot Check
                                               ┌──────────────┴────────────┐
                                               │   AI ANPR Worker Engine   │
                                               │   - YOLOv8 Detection      │
                                               │   - PaddleOCR Extraction  │
                                               │   - Plate Normalizer      │
                                               └───────────────────────────┘
```

---

## 📁 Repository Structure

```text
Project-Sentinel/
├── docker-compose.yml              # 6-service microservice orchestration
├── README.md                       # Comprehensive system documentation
├── .env.example                    # Environment variable configuration template
├── .gitignore                      # Git exclusion rules
│
├── backend/                        # FastAPI REST APIs, GIS DB & Trajectory Core
│   ├── main.py                     # App lifespan, CORS, middleware, router mount
│   ├── config.py                   # Pydantic BaseSettings environment loader
│   ├── Dockerfile                  # Production container definition
│   ├── requirements.txt            # Python dependencies (FastAPI, SQLAlchemy, etc.)
│   ├── api/
│   │   ├── cameras.py              # Model 1: GIS Asset Registry & onboarding APIs
│   │   ├── tracking.py             # Route Trajectory Engine (Haversine geodesic)
│   │   ├── analytics.py            # ANPR detections & live watchlist endpoints
│   │   ├── websockets.py           # Real-time WebSocket ConnectionManager
│   │   └── auth.py                 # API Key validator & RTSP SSRF guardrails
│   ├── db/
│   │   ├── database.py             # SQLAlchemy engine & SQLite WAL config
│   │   ├── models.py               # Camera, Department, ANPRDetection, Watchlist
│   │   └── seed_data.py            # Auto-seeder with 50 camera nodes
│   └── services/
│       └── health_checker.py       # Asynchronous camera status prober
│
├── ai_engine/                      # Computer Vision ANPR & In-Memory Matching
│   ├── main.py                     # Multi-stream worker simulation loop
│   ├── anpr_processor.py           # License plate OCR & regex normalization heuristics
│   ├── watchlist_matcher.py        # Sub-1ms Redis hash lookup with memory fallback
│   ├── requirements.txt            # AI worker dependencies
│   └── Dockerfile                  # AI worker container definition
│
├── media_relay/                    # Zero-Latency RTSP-to-WebRTC Stream Relay
│   └── mediamtx.yml                # MediaMTX configuration
│
├── frontend/                       # React 18 Command Center Dashboard
│   ├── package.json                # Dependencies (React, Leaflet, Tailwind CSS)
│   ├── vite.config.js              # Vite bundler & reverse proxy rules
│   ├── index.html                  # HTML5 application shell
│   └── src/
│       ├── main.jsx                # React DOM entrypoint
│       ├── App.jsx                 # Top-level tabbed navigation & WebSocket alert listener
│       ├── index.css               # Tailwind CSS & radar ping animations
│       ├── services/
│       │   └── api.js              # Axios client with automatic offline fallback data
│       └── components/
│           ├── GISMap.jsx          # Interactive Leaflet map with custom camera pins
│           ├── RouteTracer.jsx     # Vehicle trajectory search & checkpoint timeline
│           ├── VideoWall.jsx       # 2x2 and 3x3 multi-stream live video wall
│           ├── CameraRegistry.jsx  # Searchable tabular asset registry with onboarding modal
│           └── AlertBanner.jsx     # Audio-visual emergency notification toast (880Hz chime)
│
└── scripts/                        # Automated Evaluation & Testing Tools
    ├── run_step4_demo.py           # Vehicle trajectory simulation trigger
    ├── test_all_components.py      # Automated 6-point unittest test suite
    └── generate_50_streams.py      # Baseline camera stream ingestion verification
```

---

## 🚀 Quick Start Guide

### Option 1: Docker Compose (Recommended)

Run all 6 microservices (PostGIS, Redis, MediaMTX, Backend, AI Engine, Frontend) with a single command:

```bash
# 1. Clone the repository
git clone https://github.com/nidhishakolkar01-lgtm/Project-Sentinel.git
cd Project-Sentinel

# 2. Build and launch all containers
docker-compose up --build -d

# 3. Access the services:
# - Command Center UI:  http://localhost
# - Backend REST API:   http://localhost:8000
# - Interactive Docs:   http://localhost:8000/docs
# - MediaMTX WebRTC:    http://localhost:8889
```

---

### Option 2: Local Development Setup (Zero Docker Required)

#### Prerequisites
* **Python**: 3.10 or higher
* **Node.js**: 18.0 or higher
* **npm**: 9.0 or higher

#### Step 1: Start the Backend Service
```bash
cd backend

# Create and activate virtual environment (optional but recommended)
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Launch FastAPI server (auto-seeds 50 cameras on first boot)
python main.py
```
* Backend API: `http://localhost:8000`
* Interactive API Documentation (Swagger): `http://localhost:8000/docs`

#### Step 2: Start the AI Worker Engine (in a new terminal)
```bash
cd ai_engine
pip install -r requirements.txt
python main.py
```

#### Step 3: Start the Frontend Command Center (in a new terminal)
```bash
cd frontend
npm install
npm run dev
```
* Dashboard URL: `http://localhost:3000`

---

## 📡 API Documentation

FastAPI provides an automatic, interactive Swagger UI available at `/docs` when the backend is running.

### Key Endpoints

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `GET` | `/` | System health, version & architecture status | No |
| `GET` | `/api/v1/cameras` | List all cameras (supports `district`, `department`, `status` filters) | No |
| `POST`| `/api/v1/cameras/onboard` | Onboard a new camera asset into the GIS registry (SSRF protected) | `X-API-Key` |
| `GET` | `/api/v1/cameras/{id}` | Retrieve individual camera metadata by ID | No |
| `GET` | `/api/v1/tracking/route` | Compute chronological route trajectory for a target license plate | No |
| `GET` | `/api/v1/analytics/detections` | Paginated feed of latest ANPR vehicle detections | No |
| `POST`| `/api/v1/analytics/watchlist` | Add or update a license plate on the active watchlist | `X-API-Key` |
| `GET` | `/api/v1/analytics/watchlist` | Fetch all active watchlist entries | No |
| `WS`  | `/ws/alerts` | Full-duplex WebSocket stream for real-time watchlist match notifications | No |

### Sample Route Trajectory Response (`GET /api/v1/tracking/route?plate=GJ01HK9988`)

```json
{
  "target_plate": "GJ01HK9988",
  "total_checkpoints": 4,
  "total_distance_km": 38.45,
  "first_seen": "2026-10-24T17:15:00Z",
  "last_seen": "2026-10-24T17:55:00Z",
  "trajectory": [
    {
      "sequence": 1,
      "camera_id": 4,
      "camera_code": "CAM-AHM-004",
      "location_name": "Geeta Mandir Central Bus Stand",
      "district": "Ahmedabad",
      "latitude": 23.0124,
      "longitude": 72.5941,
      "detected_plate": "GJ01HK9988",
      "timestamp": "2026-10-24T17:15:00Z",
      "confidence": 0.98,
      "snapshot_url": "/snapshots/demo_CAM-AHM-004.jpg"
    },
    {
      "sequence": 2,
      "camera_id": 5,
      "camera_code": "CAM-AHM-005",
      "location_name": "Narol Circle - Highway Junction",
      "district": "Ahmedabad",
      "latitude": 22.9734,
      "longitude": 72.6012,
      "detected_plate": "GJ01HK9988",
      "timestamp": "2026-10-24T17:30:00Z",
      "confidence": 0.96,
      "snapshot_url": "/snapshots/demo_CAM-AHM-005.jpg"
    }
  ]
}
```

---

## 🧪 Interactive Evaluation & Demo

### 1. Vehicle Route Trajectory Demonstration
To run the automated vehicle route reconstruction simulation:
```bash
python scripts/run_step4_demo.py
```
This script:
1. Injects target vehicle `GJ01HK9988` into the live watchlist as a `CRITICAL` stolen vehicle alert.
2. Simulates chronological ANPR hits across regional highway CCTV checkpoints.
3. Calculates the geodesic route path and distance using the Haversine formula.

Open the web dashboard at `http://localhost:3000`, switch to the **Step 4 Route Tracer** tab, enter `GJ01HK9988`, and click **Trace Trajectory** to see the route polyline snap across the interactive GIS map.

### 2. Running Automated Unit & Integration Tests
Project Sentinel includes a comprehensive test suite validating all major endpoints, SSRF rejection rules, route math, and WebSocket heartbeats:

```bash
python scripts/test_all_components.py
```

Expected test results:
```text
============================================================
RUNNING COMPREHENSIVE SENTINEL AUDIT & COMPONENT TESTS
============================================================
test_01_root_endpoint (test_all_components.TestSentinelPlatform.test_01_root_endpoint) ... ok
test_02_list_cameras (test_all_components.TestSentinelPlatform.test_02_list_cameras) ... ok
test_03_route_tracing_step4 (test_all_components.TestSentinelPlatform.test_03_route_tracing_step4) ... ok
test_04_ssrf_url_validation_rejection (test_all_components.TestSentinelPlatform.test_04_ssrf_url_validation_rejection) ... ok
test_05_watchlist_management (test_all_components.TestSentinelPlatform.test_05_watchlist_management) ... ok
test_06_websocket_heartbeat (test_all_components.TestSentinelPlatform.test_06_websocket_heartbeat) ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.812s

OK
```

---

## 🔒 Security & Defensive Design

* **Server-Side Request Forgery (SSRF) Protection**: All incoming camera RTSP stream URLs submitted via `/api/v1/cameras/onboard` are validated against strict scheme requirements (`rtsp://`, `rtsps://`, `http://`, `https://`) and sanitized to prevent loopback and unauthorized internal network scanning.
* **API Key Guardrails**: Mutating operations (onboarding camera nodes, adding watchlist plates) require authentication via the `X-API-Key` request header.
* **Database Concurrency (SQLite WAL Mode)**: When running in development on SQLite, the system automatically enables Write-Ahead Logging (`PRAGMA journal_mode=WAL;`) with a 5000ms busy timeout to prevent write locks during high-throughput concurrent ANPR ingestion.
* **Resilient Graceful Degradation**: 
  * If Redis is unreachable, the AI Engine seamlessly falls back to an internal in-memory watchlist dictionary.
  * If the Backend API is temporarily offline, the React frontend falls back to pre-seeded mock GIS camera data without crashing the UI.

---

## 📊 Tech Stack Summary

* **Frontend**: React 18, React-Leaflet, Leaflet 1.9, Tailwind CSS, Lucide Icons, Axios, Web Audio API
* **Backend**: Python 3.11, FastAPI, SQLAlchemy 2.0, Pydantic V2, Uvicorn, WebSockets
* **Data Stores**: PostgreSQL 15 / PostGIS 3.3, SQLite 3 (WAL mode), Redis 7 (Alpine)
* **Media & Relay**: MediaMTX (bluenviron), WebRTC, RTSP, HLS
* **AI & Computer Vision**: YOLOv8 (Vehicle Detection), PaddleOCR (License Plate Recognition), NumPy, OpenCV
* **Deployment**: Docker, Docker Compose

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

<div align="center">
Developed as an advanced engineering demonstration of distributed video analytics, geospatial intelligence, and low-latency stream processing.
</div>
