"""
In-Memory Event Publisher for Phase 5 (Fallback when Kafka is not available)
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Callable
from datetime import datetime
from .schemas import BaseEvent, create_event

logger = logging.getLogger(__name__)


class InMemoryEventPublisher:
    """In-memory event publisher for development/fallback"""
    
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.event_history: List[Dict[str, Any]] = []
        self.max_history = 1000
    
    async def start(self):
        """Start the in-memory publisher"""
        logger.info("In-memory event publisher started")
    
    async def stop(self):
        """Stop the in-memory publisher"""
        logger.info("In-memory event publisher stopped")
    
    def subscribe(self, event_type: str, callback: Callable):
        """Subscribe to events of a specific type"""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)
    
    async def publish_event(self, event: BaseEvent) -> bool:
        """Publish an event to subscribers"""
        try:
            event_data = event.model_dump()
            
            # Store in history
            self.event_history.append(event_data)
            if len(self.event_history) > self.max_history:
                self.event_history.pop(0)
            
            # Notify subscribers
            event_type = event.event_type
            if event_type in self.subscribers:
                for callback in self.subscribers[event_type]:
                    try:
                        if asyncio.iscoroutinefunction(callback):
                            await callback(event_data)
                        else:
                            callback(event_data)
                    except Exception as e:
                        logger.error(f"Error in event subscriber: {e}")
            
            # Also notify wildcard subscribers
            if "*" in self.subscribers:
                for callback in self.subscribers["*"]:
                    try:
                        if asyncio.iscoroutinefunction(callback):
                            await callback(event_data)
                        else:
                            callback(event_data)
                    except Exception as e:
                        logger.error(f"Error in wildcard subscriber: {e}")
            
            logger.info(f"Published event {event_type} to {len(self.subscribers.get(event_type, []))} subscribers")
            return True
            
        except Exception as e:
            logger.error(f"Error publishing event {event.event_type}: {e}")
            return False
    
    async def publish_task_created(self, task_id: int, user_id: str, task_data: Dict[str, Any]) -> bool:
        """Publish task created event"""
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
    
    def get_event_history(self, event_type: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get event history"""
        if event_type:
            filtered = [e for e in self.event_history if e.get("event_type") == event_type]
            return filtered[-limit:]
        return self.event_history[-limit:]


# Global in-memory publisher instance
_memory_publisher: InMemoryEventPublisher = None


async def get_memory_publisher() -> InMemoryEventPublisher:
    """Get or create the global in-memory event publisher"""
    global _memory_publisher
    if _memory_publisher is None:
        _memory_publisher = InMemoryEventPublisher()
        await _memory_publisher.start()
    return _memory_publisher