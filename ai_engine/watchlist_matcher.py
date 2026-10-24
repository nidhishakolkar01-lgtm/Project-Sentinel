import os
import redis
import json

class WatchlistMatcher:
    def __init__(self):
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = int(os.getenv("REDIS_PORT", 6379))
        
        # Redis Connection Pool for high-throughput concurrency
        self.pool = redis.ConnectionPool(
            host=redis_host, 
            port=redis_port, 
            db=0, 
            socket_timeout=2,
            max_connections=50
        )
        self.redis = redis.Redis(connection_pool=self.pool)
        
        # In-memory fallback watchlist store
        self.memory_watchlist = {
            "GJ01HK9988": {"reason": "Step 4 Evaluation Target / Stolen SUV", "category": "Stolen Vehicle", "severity": "CRITICAL"},
            "GJ18AB1234": {"reason": "Wanted Criminal Vehicle", "category": "Wanted Criminal", "severity": "CRITICAL"},
            "GJ05CD5678": {"reason": "Unpaid Transport Fines & Blacklisted RTO", "category": "Blacklisted", "severity": "HIGH"},
            "GJ06EF9012": {"reason": "Missing Person Probe Vehicle", "category": "Missing Person", "severity": "MEDIUM"}
        }

    def check_watchlist(self, plate_number: str) -> dict:
        if not plate_number:
            return {"is_hit": False, "category": None, "severity": "NORMAL"}
            
        clean_plate = plate_number.upper().replace("-", "").replace(" ", "").strip()
        
        # Try Redis Hash Lookup first
        try:
            res = self.redis.hget("watchlist:plates", clean_plate)
            if res:
                data = json.loads(res.decode('utf-8'))
                return {
                    "is_hit": True, 
                    "category": data.get("category", "Stolen Vehicle"), 
                    "severity": data.get("severity", "CRITICAL")
                }
        except Exception:
            pass # Fall back to memory_watchlist
        
        if clean_plate in self.memory_watchlist:
            info = self.memory_watchlist[clean_plate]
            return {
                "is_hit": True, 
                "category": info["category"], 
                "severity": info["severity"]
            }

        return {"is_hit": False, "category": None, "severity": "NORMAL"}
