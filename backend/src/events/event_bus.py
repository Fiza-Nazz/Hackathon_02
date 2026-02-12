"""
Event Bus for Phase V - Supports both In-Memory and Kafka
"""
import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass, asdict
import uuid

logger = logging.getLogger(__name__)

@dataclass
class Event:
    event_id: str
    event_type: str
    aggregate_id: str
    user_id: str
    timestamp: datetime
    data: Dict[str, Any]
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class EventBus:
    """Hybrid event bus supporting both in-memory and Kafka"""
    
    def __init__(self, use_kafka: bool = False):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.events: List[Event] = []
        self.running = True
        self.use_kafka = use_kafka
        self.kafka_publisher = None
    
    async def initialize_kafka(self):
        """Initialize Kafka publisher if enabled"""
        if self.use_kafka:
            try:
                from .kafka_publisher import get_kafka_publisher
                self.kafka_publisher = await get_kafka_publisher()
                logger.info("✅ Kafka publisher initialized")
            except Exception as e:
                logger.warning(f"⚠️ Kafka initialization failed, falling back to in-memory: {e}")
                self.use_kafka = False
    
    async def publish(self, topic: str, event: Event):
        """Publish event to topic"""
        logger.info(f"📡 Publishing event: {event.event_type} to topic: {topic}")
        
        # Store event in memory
        self.events.append(event)
        
        # Publish to Kafka if enabled
        if self.use_kafka and self.kafka_publisher:
            try:
                await self.kafka_publisher.publish(topic, event)
            except Exception as e:
                logger.error(f"❌ Kafka publish failed: {e}")
        
        # Notify in-memory subscribers
        if topic in self.subscribers:
            for callback in self.subscribers[topic]:
                try:
                    await callback(event)
                except Exception as e:
                    logger.error(f"❌ Error in subscriber: {e}")
    
    def subscribe(self, topic: str, callback: Callable):
        """Subscribe to topic"""
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(callback)
        logger.info(f"✅ Subscribed to topic: {topic}")
    
    def get_events(self, topic: str = None, event_type: str = None) -> List[Event]:
        """Get events by topic or type"""
        filtered_events = self.events
        
        if event_type:
            filtered_events = [e for e in filtered_events if e.event_type == event_type]
            
        return filtered_events


# Global event bus instance
event_bus = EventBus(use_kafka=False)  # Start with in-memory, can be enabled later

# Event Types
class TaskEvents:
    CREATED = "task.created"
    UPDATED = "task.updated"
    COMPLETED = "task.completed"
    DELETED = "task.deleted"

class ReminderEvents:
    SCHEDULED = "reminder.scheduled"
    DUE = "reminder.due"
    SENT = "reminder.sent"

# Topics
class Topics:
    TASK_EVENTS = "task-events"
    REMINDERS = "reminders"
    TASK_UPDATES = "task-updates"

# Helper functions
async def publish_task_event(event_type: str, task_id: int, user_id: str, task_data: Dict[str, Any]):
    """Publish task-related event"""
    event = Event(
        event_id=str(uuid.uuid4()),
        event_type=event_type,
        aggregate_id=str(task_id),
        user_id=user_id,
        timestamp=datetime.utcnow(),
        data=task_data
    )
    
    await event_bus.publish(Topics.TASK_EVENTS, event)
    await event_bus.publish(Topics.TASK_UPDATES, event)  # For real-time updates

async def publish_reminder_event(task_id: int, user_id: str, remind_at: datetime, task_title: str):
    """Publish reminder event"""
    event = Event(
        event_id=str(uuid.uuid4()),
        event_type=ReminderEvents.SCHEDULED,
        aggregate_id=str(task_id),
        user_id=user_id,
        timestamp=datetime.utcnow(),
        data={
            "task_id": task_id,
            "title": task_title,
            "remind_at": remind_at.isoformat(),
            "user_id": user_id
        }
    )
    
    await event_bus.publish(Topics.REMINDERS, event)

# Initialize event handlers
async def init_event_handlers():
    """Initialize all event handlers"""
    from .handlers import (
        handle_task_created,
        handle_task_completed,
        handle_reminder_due
    )
    
    # Subscribe to events
    event_bus.subscribe(Topics.TASK_EVENTS, handle_task_created)
    event_bus.subscribe(Topics.TASK_EVENTS, handle_task_completed)
    event_bus.subscribe(Topics.REMINDERS, handle_reminder_due)
    
    print("✅ Event handlers initialized")