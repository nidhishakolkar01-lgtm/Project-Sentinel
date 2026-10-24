import json
import asyncio
from typing import List
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(tags=["Real-Time WebSockets Alert Gateway"])

class ConnectionManager:
    def __init__(self, max_connections: int = 500):
        self.active_connections: List[WebSocket] = []
        self.max_connections = max_connections

    async def connect(self, websocket: WebSocket):
        if len(self.active_connections) >= self.max_connections:
            await websocket.close(code=1008, reason="Connection limit exceeded")
            return False
        
        await websocket.accept()
        self.active_connections.append(websocket)
        return True

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        """Broadcasts JSON payload to all active clients and prunes stale connections."""
        to_remove = []
        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)
            except Exception:
                to_remove.append(connection)
        
        # Prune dropped connection handles
        for dead_conn in to_remove:
            self.disconnect(dead_conn)

manager = ConnectionManager()

@router.websocket("/ws/alerts")
async def websocket_alerts_endpoint(websocket: WebSocket):
    connected = await manager.connect(websocket)
    if not connected:
        return

    try:
        while True:
            # Heartbeat ping/pong loop
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except (WebSocketDisconnect, RuntimeError):
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)

async def push_alert_event(alert_payload: dict):
    await manager.broadcast(alert_payload)
