"""
Recurring Task Service for Phase 5 Event-Driven Architecture
Handles creation of recurring task instances
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from aiokafka.errors import KafkaError
import signal
import os
import sys

# Add backend to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from backend.src.database.database import get_engine
from backend.src.models.task import Task, TaskTag
from sqlmodel import Session, select

logger = logging.getLogger(__name__)


class RecurringTaskService:
    """Handles recurring task creation based on completion events"""
    
    def __init__(self, kafka_servers: str = "localhost:19092"):
        self.kafka_servers = kafka_servers
        self.consumer: AIOKafkaConsumer = None
        self.producer: AIOKafkaProducer = None
        self.running = False
    
    async def start(self):
        """Start the recurring task service"""
        self.running = True
        
        # Start Kafka consumer and producer
        await self.start_kafka_consumer()
        await self.start_kafka_producer()
        
        logger.info("Recurring task service started")
        
        # Start consuming events
        await self.consume_events()
    
    async def start_kafka_consumer(self):
        """Start Kafka consumer for task completion events"""
        try:
            self.consumer = AIOKafkaConsumer(
                "task-events",
                bootstrap_servers=self.kafka_servers,
                group_id="recurring-task-service",
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                auto_offset_reset='latest'
            )
            await self.consumer.start()
            logger.info("Kafka consumer started for recurring task service")
        except Exception as e:
            logger.error(f"Failed to start Kafka consumer: {e}")
            raise
    
    async def start_kafka_producer(self):
        """Start Kafka producer for publishing new task events"""
        try:
            self.producer = AIOKafkaProducer(
                bootstrap_servers=self.kafka_servers,
                value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8')
            )
            await self.producer.start()
            logger.info("Kafka producer started for recurring task service")
        except Exception as e:
            logger.error(f"Failed to start Kafka producer: {e}")
            raise
    
    async def consume_events(self):
        """Consume and process task completion events"""
        try:
            async for message in self.consumer:
                if not self.running:
                    break
                
                try:
                    event_data = message.value
                    event_type = event_data.get("event_type")
                    
                    if event_type == "task.completed":
                        await self.handle_task_completed(event_data)
                        
                except Exception as e:
                    logger.error(f"Error processing event: {e}")
                    
        except Exception as e:
            logger.error(f"Error in event consumption: {e}")
    
    async def handle_task_completed(self, event_data: Dict[str, Any]):
        """Handle task completion and create next recurring instance if needed"""
        data = event_data.get("data", {})
        task_id = data.get("task_id")
        
        if not task_id:
            return
        
        try:
            with Session(get_engine()) as session:
                # Get the completed task
                task = session.get(Task, task_id)
                if not task or not task.is_recurring:
                    return
                
                logger.info(f"Processing recurring task completion: {task_id}")
                
                # Calculate next due date based on recurring pattern
                next_due_date = self.calculate_next_due_date(
                    task.due_date or datetime.utcnow(),
                    task.recurring_pattern,
                    task.recurring_interval
                )
                
                # Create new task instance
                new_task = Task(
                    title=task.title,
                    description=task.description,
                    completed=False,
                    priority=task.priority,
                    category=task.category,
                    due_date=next_due_date,
                    is_recurring=True,
                    recurring_pattern=task.recurring_pattern,
                    recurring_interval=task.recurring_interval,
                    parent_task_id=task.id,
                    user_id=task.user_id
                )
                
                session.add(new_task)
                session.commit()
                session.refresh(new_task)
                
                # Copy tags from original task
                original_tags = session.exec(
                    select(TaskTag).where(TaskTag.task_id == task_id)
                ).all()
                
                for tag in original_tags:
                    new_tag = TaskTag(
                        task_id=new_task.id,
                        tag_name=tag.tag_name
                    )
                    session.add(new_tag)
                
                session.commit()
                
                # Publish recurring task created event
                await self.publish_recurring_task_created(new_task, task)
                
                logger.info(f"Created recurring task instance: {new_task.id} from parent {task_id}")
                
        except Exception as e:
            logger.error(f"Error creating recurring task instance: {e}")
    
    def calculate_next_due_date(self, current_due_date: datetime, pattern: str, interval: int) -> datetime:
        """Calculate the next due date based on recurring pattern"""
        if pattern == "daily":
            return current_due_date + timedelta(days=interval)
        elif pattern == "weekly":
            return current_due_date + timedelta(weeks=interval)
        elif pattern == "monthly":
            # Approximate monthly calculation
            return current_due_date + timedelta(days=30 * interval)
        elif pattern == "yearly":
            # Approximate yearly calculation
            return current_due_date + timedelta(days=365 * interval)
        else:
            # Default to daily if pattern is unknown
            return current_due_date + timedelta(days=1)
    
    async def publish_recurring_task_created(self, new_task: Task, parent_task: Task):
        """Publish event for newly created recurring task"""
        event_data = {
            "event_id": f"recurring-{new_task.id}",
            "event_type": "recurring_task.created",
            "aggregate_id": str(new_task.id),
            "user_id": new_task.user_id,
            "timestamp": datetime.utcnow().isoformat(),
            "data": {
                "task_id": new_task.id,
                "title": new_task.title,
                "parent_task_id": parent_task.id,
                "recurring_pattern": new_task.recurring_pattern,
                "due_date": new_task.due_date.isoformat() if new_task.due_date else None,
                "user_id": new_task.user_id
            }
        }
        
        try:
            await self.producer.send_and_wait("task-events", value=event_data)
            logger.info(f"Published recurring task created event for task {new_task.id}")
        except Exception as e:
            logger.error(f"Error publishing recurring task event: {e}")
    
    async def stop(self):
        """Stop the recurring task service"""
        self.running = False
        
        if self.consumer:
            await self.consumer.stop()
        
        if self.producer:
            await self.producer.stop()
        
        logger.info("Recurring task service stopped")


async def main():
    """Main function to run the recurring task service"""
    logging.basicConfig(level=logging.INFO)
    
    service = RecurringTaskService()
    
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
        logger.info("Shutting down recurring task service...")
        await service.stop()


if __name__ == "__main__":
    asyncio.run(main())