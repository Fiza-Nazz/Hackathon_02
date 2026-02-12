"""
WebSocket service for real-time task updates
"""

import json
import logging
from typing import Set, Dict
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ws", tags=["websocket"])


class ConnectionManager:
    """Manage WebSocket connections"""
    
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str):
        """Accept and register a WebSocket connection"""
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        self.active_connections[user_id].add(websocket)
        logger.info(f"✅ WebSocket connected for user {user_id}")
    
    async def disconnect(self, websocket: WebSocket, user_id: str):
        """Unregister a WebSocket connection"""
        if user_id in self.active_connections:
            self.active_connections[user_id].discard(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        logger.info(f"✅ WebSocket disconnected for user {user_id}")
    
    async def broadcast_to_user(self, user_id: str, message: dict):
        """Broadcast message to all connections of a user"""
        if user_id in self.active_connections:
            disconnected = set()
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"❌ Error sending message: {e}")
                    disconnected.add(connection)
            
            # Remove disconnected connections
            for connection in disconnected:
                self.active_connections[user_id].discard(connection)
    
    async def broadcast_to_all(self, message: dict):
        """Broadcast message to all connected users"""
        for user_id in list(self.active_connections.keys()):
            await self.broadcast_to_user(user_id, message)
    
    def get_connection_count(self) -> int:
        """Get total number of active connections"""
        return sum(len(conns) for conns in self.active_connections.values())


# Global connection manager
connection_manager = ConnectionManager()


@router.websocket("/tasks/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """WebSocket endpoint for real-time task updates"""
    await connection_manager.connect(websocket, user_id)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            
            # Parse message
            try:
                message = json.loads(data)
                logger.debug(f"📨 Received message from {user_id}: {message}")
                
                # Handle different message types
                if message.get("type") == "ping":
                    await websocket.send_json({"type": "pong", "timestamp": datetime.utcnow().isoformat()})
                
                elif message.get("type") == "subscribe":
                    # Client subscribing to updates
                    await websocket.send_json({
                        "type": "subscribed",
                        "message": f"Subscribed to task updates",
                        "timestamp": datetime.utcnow().isoformat()
                    })
                
            except json.JSONDecodeError:
                await websocket.send_json({"error": "Invalid JSON"})
    
    except WebSocketDisconnect:
        await connection_manager.disconnect(websocket, user_id)
        logger.info(f"🔌 WebSocket disconnected for user {user_id}")


async def broadcast_task_update(user_id: str, event_type: str, task_data: dict):
    """Broadcast task update to user"""
    message = {
        "type": "task_update",
        "event_type": event_type,
        "task": task_data,
        "timestamp": datetime.utcnow().isoformat()
    }
    await connection_manager.broadcast_to_user(user_id, message)


async def broadcast_task_update_to_all(event_type: str, task_data: dict):
    """Broadcast task update to all connected users"""
    message = {
        "type": "task_update",
        "event_type": event_type,
        "task": task_data,
        "timestamp": datetime.utcnow().isoformat()
    }
    await connection_manager.broadcast_to_all(message)
