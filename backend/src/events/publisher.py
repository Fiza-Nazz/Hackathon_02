"""
Kafka Event Publisher for Phase 5 with In-Memory Fallback
"""

import json
import asyncio
from typing import Dict, Any, Optional
import logging
from .schemas import BaseEvent, create_event

logger = logging.getLogger(__name__)

# Try to import Kafka, fall back to in-memory if not available
try:
    from aiokafka import AIOKafkaProducer
    from aiokafka.errors import KafkaError
    KAFKA_AVAILABLE = True
except ImportError:
    KAFKA_AVAILABLE = False
    logger.warning("Kafka not available, using in-memory event publisher")

if not KAFKA_AVAILABLE:
    from .memory_publisher import InMemoryEventPublisher


class EventPublisher:
    """Event publisher with Kafka and in-memory fallback"""
    
    def __init__(self, bootstrap_servers: str = "localhost:19092", use_kafka: bool = True):
        self.bootstrap_servers = bootstrap_servers
        self.use_kafka = use_kafka and KAFKA_AVAILABLE
        self.producer: Optional[AIOKafkaProducer] = None
        self.memory_publisher: Optional[InMemoryEventPublisher] = None
        self._topics = {
            "task-events": "task-events",
            "reminders": "reminders", 
            "notifications": "notifications",
            "audit": "audit-log"
        }
    
    async def start(self):
        """Start the event publisher"""
        if self.use_kafka:
            await self._start_kafka()
        else:
            await self._start_memory()
    
    async def _start_kafka(self):
        """Start Kafka producer"""
        try:
            self.producer = AIOKafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None,
                retry_backoff_ms=1000,
                request_timeout_ms=10000,  # Reduced timeout
                enable_idempotence=True
            )
            await asyncio.wait_for(self.producer.start(), timeout=5.0)
            logger.info(f"Kafka producer started: {self.bootstrap_servers}")
        except Exception as e:
            logger.warning(f"Kafka producer failed, falling back to in-memory: {e}")
            self.use_kafka = False
            await self._start_memory()
    
    async def _start_memory(self):
        """Start in-memory publisher"""
        if not KAFKA_AVAILABLE:
            from .memory_publisher import get_memory_publisher
            self.memory_publisher = await get_memory_publisher()
        else:
            from .memory_publisher import InMemoryEventPublisher
            self.memory_publisher = InMemoryEventPublisher()
            await self.memory_publisher.start()
        logger.info("In-memory event publisher started")
    
    async def stop(self):
        """Stop the event publisher"""
        if self.producer:
            await self.producer.stop()
            logger.info("Kafka producer stopped")
        if self.memory_publisher:
            await self.memory_publisher.stop()
    
    async def publish_event(self, event: BaseEvent, topic: Optional[str] = None) -> bool:
        """Publish an event"""
        if self.use_kafka and self.producer:
            return await self._publish_kafka(event, topic)
        elif self.memory_publisher:
            return await self.memory_publisher.publish_event(event)
        else:
            logger.error("No event publisher available")
            return False
    
    async def _publish_kafka(self, event: BaseEvent, topic: Optional[str] = None) -> bool:
        """Publish event to Kafka"""
        try:
            # Determine topic based on event type
            if not topic:
                if event.event_type.startswith("task."):
                    topic = self._topics["task-events"]
                elif event.event_type.startswith("reminder."):
                    topic = self._topics["reminders"]
                else:
                    topic = self._topics["notifications"]
            
            # Prepare event data
            event_data = event.model_dump()
            
            # Use aggregate_id as partition key for ordering
            partition_key = event.aggregate_id
            
            # Send to Kafka
            await self.producer.send_and_wait(
                topic=topic,
                key=partition_key,
                value=event_data,
                headers=[
                    ("event_type", event.event_type.encode()),
                    ("user_id", event.user_id.encode()),
                    ("correlation_id", (event.correlation_id or "").encode())
                ]
            )
            
            logger.info(f"Published event {event.event_type} to Kafka topic {topic}")
            return True
            
        except Exception as e:
            logger.error(f"Kafka error publishing event {event.event_type}: {e}")
            # Fall back to in-memory
            if self.memory_publisher:
                return await self.memory_publisher.publish_event(event)
            return False
    
    async def publish_task_created(self, task_id: int, user_id: str, task_data: Dict[str, Any]) -> bool:
        """Publish task created event"""
        if self.memory_publisher:
            return await self.memory_publisher.publish_task_created(task_id, user_id, task_data)
        
        event = create_event(
            event_type="task.created",
            aggregate_id=str(task_id),
            user_id=user_id,
            data={
                "task_id": task_id,
                "title": task_data.get("title"),
                "description": task_data.get("description"),
                "priority": task_data.get("priority", "medium"),
                "category": task_data.get("category", "General"),
                "tags": task_data.get("tags", []),
                "due_date": task_data.get("due_date"),
                "is_recurring": task_data.get("is_recurring", False),
                "user_id": user_id
            }
        )
        return await self.publish_event(event)
    
    async def publish_task_completed(self, task_id: int, user_id: str, task_data: Dict[str, Any]) -> bool:
        """Publish task completed event"""
        if self.memory_publisher:
            return await self.memory_publisher.publish_task_completed(task_id, user_id, task_data)
        
        event = create_event(
            event_type="task.completed",
            aggregate_id=str(task_id),
            user_id=user_id,
            data={
                "task_id": task_id,
                "title": task_data.get("title"),
                "completed_at": task_data.get("completed_at"),
                "was_overdue": task_data.get("was_overdue", False),
                "user_id": user_id
            }
        )
        return await self.publish_event(event)
    
    async def publish_task_priority_changed(self, task_id: int, user_id: str, old_priority: str, new_priority: str, title: str) -> bool:
        """Publish task priority changed event"""
        if self.memory_publisher:
            return await self.memory_publisher.publish_task_priority_changed(task_id, user_id, old_priority, new_priority, title)
        
        event = create_event(
            event_type="task.priority_changed",
            aggregate_id=str(task_id),
            user_id=user_id,
            data={
                "task_id": task_id,
                "title": title,
                "old_priority": old_priority,
                "new_priority": new_priority,
                "changed_by": user_id,
                "user_id": user_id
            }
        )
        return await self.publish_event(event)
    
    async def publish_task_tags_updated(self, task_id: int, user_id: str, title: str, added_tags: list, removed_tags: list, current_tags: list) -> bool:
        """Publish task tags updated event"""
        if self.memory_publisher:
            return await self.memory_publisher.publish_task_tags_updated(task_id, user_id, title, added_tags, removed_tags, current_tags)
        
        event = create_event(
            event_type="task.tags_updated",
            aggregate_id=str(task_id),
            user_id=user_id,
            data={
                "task_id": task_id,
                "title": title,
                "added_tags": added_tags,
                "removed_tags": removed_tags,
                "current_tags": current_tags,
                "user_id": user_id
            }
        )
        return await self.publish_event(event)


# Global publisher instance
_publisher: Optional[EventPublisher] = None


async def get_publisher() -> EventPublisher:
    """Get or create the global event publisher"""
    global _publisher
    if _publisher is None:
        _publisher = EventPublisher()
        await _publisher.start()
    return _publisher


async def shutdown_publisher():
    """Shutdown the global event publisher"""
    global _publisher
    if _publisher:
        await _publisher.stop()
        _publisher = None