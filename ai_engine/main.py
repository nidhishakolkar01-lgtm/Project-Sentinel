import os
import time
import httpx
from anpr_processor import ANPRProcessor
from watchlist_matcher import WatchlistMatcher

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
API_KEY = os.getenv("SENTINEL_API_KEY", "sentinel_sec_key_2026_auth")

def run_ai_engine():
    print("[AI Engine] Sentinel Multi-Stream AI ANPR Engine Starting...")
    processor = ANPRProcessor()
    matcher = WatchlistMatcher()
    
    # Step 4 Demo Simulation Stream Loop
    demo_sequence = [
        ("CAM-AHM-004", "GJ01HK9988", "Geeta Mandir Bus Stand, Ahmedabad"),
        ("CAM-AHM-005", "GJ01HK9988", "Narol Circle Highway Junction, Ahmedabad"),
        ("CAM-AHM-015", "GJ01HK9988", "Sanand Toll Plaza, Ahmedabad"),
        ("CAM-GND-016", "GJ01HK9988", "Infocity Gate Sector 0, Gandhinagar")
    ]

    seq_idx = 0
    headers = {"X-API-Key": API_KEY}
    client = httpx.Client(timeout=5, headers=headers)

    while True:
        try:
            cam_code, plate, loc = demo_sequence[seq_idx % len(demo_sequence)]
            seq_idx += 1

            clean_plate = processor.normalize_plate(plate)
            match_res = matcher.check_watchlist(clean_plate)

            if match_res["is_hit"]:
                alert_payload = {
                    "event_type": "WATCHLIST_MATCH_ALERT",
                    "severity": match_res["severity"],
                    "data": {
                        "detected_plate": clean_plate,
                        "watchlist_category": match_res["category"],
                        "confidence_score": 0.96,
                        "camera_code": cam_code,
                        "location_name": loc,
                        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
                    }
                }
                print(f"🔥 [AI ENGINE ALERT] MATCH DETECTED! Plate: {clean_plate} at {cam_code} ({loc})")
                
                # Push alert to Backend Analytics API
                try:
                    res = client.post(
                        f"{BACKEND_URL}/api/v1/analytics/watchlist",
                        json={
                            "plate_number": clean_plate,
                            "reason": f"AI Engine Live Alert at {cam_code}",
                            "category": match_res["category"],
                            "severity": match_res["severity"]
                        }
                    )
                except Exception as ex:
                    print(f"[AI Engine] Telemetry push note: {ex}")

        except Exception as e:
            print(f"[AI Engine] Stream processing loop error: {e}")

        time.sleep(10)

if __name__ == "__main__":
    run_ai_engine()
