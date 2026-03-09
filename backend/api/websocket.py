from fastapi import WebSocket, Query, HTTPException, APIRouter
from typing import List
import json
from datetime import datetime

router = APIRouter()

class WSManager:
    def __init__(self):
        self.connections: List[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.connections.append(ws)

    async def broadcast(self, event_type: str, payload: dict):
        msg = json.dumps({
            'event': event_type,
            'data': payload,
            'ts': datetime.now().isoformat()
        })
        dead = []
        for ws in self.connections:
            try:
                await ws.send_text(msg)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.connections.remove(ws)

ws_manager = WSManager()

@router.websocket('/live')
async def ws_endpoint(websocket: WebSocket, token: str = Query(...)):
    # Mock token validation
    # if token != settings.DASHBOARD_TOKEN:
    #     await websocket.close(code=1008)  # Policy violation
    #     return
    await ws_manager.connect(websocket)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except Exception:
        if websocket in ws_manager.connections:
            ws_manager.connections.remove(websocket)
