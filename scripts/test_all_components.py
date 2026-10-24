import os
import sys
import unittest

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from fastapi.testclient import TestClient
from main import app
from db.database import engine, Base
from db.seed_data import init_db

class TestSentinelPlatform(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        init_db() # Seed 50 Gujarat Cameras, Departments, and Step 4 Watchlist
        cls.client = TestClient(app)

    def test_01_root_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "ONLINE")
        self.assertIn("Model 5", data["model_architecture"])

    def test_02_list_cameras(self):
        response = self.client.get("/api/v1/cameras")
        self.assertEqual(response.status_code, 200)
        cameras = response.json()
        self.assertIsInstance(cameras, list)
        self.assertGreaterEqual(len(cameras), 1)

    def test_03_route_tracing_step4(self):
        response = self.client.get("/api/v1/tracking/route?plate=GJ01HK9988")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["target_plate"], "GJ01HK9988")
        self.assertGreaterEqual(data["total_checkpoints"], 1)
        self.assertIsInstance(data["trajectory"], list)

    def test_04_ssrf_url_validation_rejection(self):
        # Attempt to onboard a camera with disallowed scheme or malformed URL
        payload = {
            "camera_code": "CAM-TEST-BAD",
            "department_name": "Test Dept",
            "vendor_name": "Hikvision",
            "rtsp_url": "ftp://malicious-host:21/stream",
            "latitude": 23.0,
            "longitude": 72.0,
            "district": "Ahmedabad",
            "installation_address": "Test Address"
        }
        response = self.client.post("/api/v1/cameras/onboard", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid stream scheme", response.json()["detail"])

    def test_05_watchlist_management(self):
        payload = {
            "plate_number": "GJ99ZZ0000",
            "reason": "Automated Security Audit Test Vehicle",
            "category": "Stolen Vehicle",
            "severity": "CRITICAL"
        }
        response = self.client.post("/api/v1/analytics/watchlist", json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["plate_number"], "GJ99ZZ0000")

    def test_06_websocket_heartbeat(self):
        with self.client.websocket_connect("/ws/alerts") as websocket:
            websocket.send_text("ping")
            data = websocket.receive_text()
            self.assertEqual(data, "pong")

if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING COMPREHENSIVE SENTINEL AUDIT & COMPONENT TESTS")
    print("=" * 60)
    unittest.main()
