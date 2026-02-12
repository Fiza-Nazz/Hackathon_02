"""
Notification Service for Phase 5 Event-Driven Architecture
Handles reminder notifications and real-time updates
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any, Set
from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaError
import websockets
from websockets.server import WebSocketServerProtocol
import signal

logger = logging.getLogger(__name__)


class NotificationService:
    """Handles notifications and real-time updates"""
    
    def __init__(self, kafka_servers: str = "localhost:19092", websocket_port: int = 8765):
        self.kafka_servers = kafka_servers
        self.websocket_port = websocket_port
        self.consumer: AIOKafkaConsumer = None
        self.websocket_clients: Set[WebSocketServerProtocol] = set()
        self.running = False
    
    async def start(self):
        """Start the notification service"""
        self.running = True
        
        # Start Kafka consumer
        await self.start_kafka_consumer()
        
        # Start WebSocket server
        websocket_server = await websockets.serve(
            self.handle_websocket_connection,
            "localhost",
            self.websocket_port
        )
        
        logger.info(f"Notification service started on WebSocket port {self.websocket_port}")
        
        # Start consuming events
        await self.consume_events()
    
    async def start_kafka_consumer(self):
        """Start Kafka consumer for notifications"""
        try:
            self.consumer = AIOKafkaConsumer(
                "reminders",
                "notifications", 
                "task-events",
                bootstrap_servers=self.kafka_servers,
                group_id="notification-service",
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                auto_offset_reset='latest'
            )
            await self.consumer.start()
            logger.info("Kafka consumer started for notification service")
        except Exception as e:
            logger.error(f"Failed to start Kafka consumer: {e}")
            raise
    
    async def handle_websocket_connection(self, websocket: WebSocketServerProtocol, path: str):
        """Handle new WebSocket connections"""
        self.websocket_clients.add(websocket)
        logger.info(f"New WebSocket client connected: {websocket.remote_address}")
        
        try:
            # Send welcome message
            await websocket.send(json.dumps({
                "type": "connection",
                "message": "Connected to notification service",
                "timestamp": datetime.utcnow().isoformat()
            }))
            
            # Keep connection alive
            await websocket.wait_closed()
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.websocket_clients.discard(websocket)
            logger.info(f"WebSocket client disconnected: {websocket.remote_address}")
    
    async def broadcast_to_websockets(self, message: Dict[str, Any]):
        """Broadcast message to all connected WebSocket clients"""
        if not self.websocket_clients:
            return
        
        message_json = json.dumps(message, default=str)
        disconnected_clients = set()
        
        for client in self.websocket_clients:
            try:
                await client.send(message_json)
            except websockets.exceptions.ConnectionClosed:
                disconnected_clients.add(client)
            except Exception as e:
                logger.error(f"Error sending to WebSocket client: {e}")
                disconnected_clients.add(client)
        
        # Remove disconnected clients
        self.websocket_clients -= disconnected_clients
    
    async def consume_events(self):
        """Consume and process events from Kafka"""
        try:
            async for message in self.consumer:
                if not self.running:
                    break
                
                try:
                    event_data = message.value
                    event_type = event_data.get("event_type")
                    
                    logger.info(f"Processing event: {event_type}")
                    
                    # Process different event types
                    if event_type == "reminder.triggered":
                        await self.handle_reminder_triggered(event_data)
                    elif event_type.startswith("task."):
                        await self.handle_task_event(event_data)
                    else:
                        await self.handle_generic_notification(event_data)
                        
                except Exception as e:
                    logger.error(f"Error processing event: {e}")
                    
        except Exception as e:
            logger.error(f"Error in event consumption: {e}")
    
    async def handle_reminder_triggered(self, event_data: Dict[str, Any]):
        """Handle reminder triggered events"""
        data = event_data.get("data", {})
        
        notification = {
            "type": "reminder",
            "title": "Task Reminder",
            "message": data.get("message", "You have a task reminder"),
            "task_id": data.get("task_id"),
            "user_id": data.get("user_id"),
            "timestamp": datetime.utcnow().isoformat(),
            "priority": "high"
        }
        
        # Broadcast to WebSocket clients
        await self.broadcast_to_websockets(notification)
        
        # Here you could also send email, SMS, push notifications, etc.
        logger.info(f"Reminder notification sent for task {data.get('task_id')}")
    
    async def handle_task_event(self, event_data: Dict[str, Any]):
        """Handle task-related events"""
        event_type = event_data.get("event_type")
        data = event_data.get("data", {})
        
        # Create real-time update notification
        notification = {
            "type": "task_update",
            "event_type": event_type,
            "task_id": data.get("task_id"),
            "user_id": event_data.get("user_id"),
            "timestamp": datetime.utcnow().isoformat(),
            "data": data
        }
        
        # Broadcast to WebSocket clients
        await self.broadcast_to_websockets(notification)
        
        logger.info(f"Task update notification sent: {event_type}")
    
    async def handle_generic_notification(self, event_data: Dict[str, Any]):
        """Handle generic notifications"""
        notification = {
            "type": "notification",
            "event_type": event_data.get("event_type"),
            "message": f"Event: {event_data.get('event_type')}",
            "timestamp": datetime.utcnow().isoformat(),
            "data": event_data.get("data", {})
        }
        
        await self.broadcast_to_websockets(notification)
    
    async def stop(self):
        """Stop the notification service"""
        self.running = False
        
        if self.consumer:
            await self.consumer.stop()
        
        # Close all WebSocket connections
        for client in self.websocket_clients.copy():
            await client.close()
        
        logger.info("Notification service stopped")


async def main():
    """Main function to run the notification service"""
    logging.basicConfig(level=logging.INFO)
    
    service = NotificationService()
    
    # Handle shutdown gracefully
    def signal_handler():
        logger.info("Received shutdown signal")
        asyncio.create_task(service.stop())
    
    # Register signal handlers
    for sig in [signal.SIGTERM, signal.SIGINT]:
        signal.signal(sig, lambda s, f: signal_handler())
    
    try:
        await service.start()
    except KeyboardInterrupt:
        logger.info("Shutting down notification service...")
        await service.stop()


if __name__ == "__main__":
    asyncio.run(main())