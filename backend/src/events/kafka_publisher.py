"""
Kafka-based event publisher for Phase 5 Event-Driven Architecture
"""

import json
import logging
from typing import Optional, Dict, Any
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from datetime import datetime
from .schemas import BaseEvent

logger = logging.getLogger(__name__)


class KafkaEventPublisher:
    """Kafka-based event publisher"""
    
    def __init__(self, bootstrap_servers: str = "localhost:19092"):
        """Initialize Kafka publisher"""
        self.bootstrap_servers = bootstrap_servers
        self.producer: Optional[AIOKafkaProducer] = None
        self.is_connected = False
        
    async def start(self):
        """Start Kafka producer"""
        try:
            self.producer = AIOKafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8')
            )
            await self.producer.start()
            self.is_connected = True
            logger.info(f"✅ Kafka producer connected to {self.bootstrap_servers}")
        except Exception as e:
            logger.error(f"❌ Failed to connect to Kafka: {e}")
            self.is_connected = False
            raise
    
    async def stop(self):
        """Stop Kafka producer"""
        if self.producer:
            await self.producer.stop()
            self.is_connected = False
            logger.info("✅ Kafka producer stopped")
    
    async def publish(self, topic: str, event: BaseEvent) -> bool:
        """Publish event to Kafka topic"""
        if not self.is_connected or not self.producer:
            logger.warning(f"⚠️ Kafka not connected, skipping publish to {topic}")
            return False
        
        try:
            event_dict = event.dict()
            # Convert datetime objects to ISO format strings
            event_dict['timestamp'] = event_dict['timestamp'].isoformat()
            
            await self.producer.send_and_wait(topic, value=event_dict)
            logger.debug(f"✅ Event published to {topic}: {event.event_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to publish event to {topic}: {e}")
            return False


class KafkaEventConsumer:
    """Kafka-based event consumer"""
    
    def __init__(self, bootstrap_servers: str = "localhost:19092", group_id: str = "default"):
        """Initialize Kafka consumer"""
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.consumer: Optional[AIOKafkaConsumer] = None
        self.is_connected = False
    
    async def start(self, topics: list):
        """Start Kafka consumer"""
        try:
            self.consumer = AIOKafkaConsumer(
                *topics,
                bootstrap_servers=self.bootstrap_servers,
                group_id=self.group_id,
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                auto_offset_reset='earliest'
            )
            await self.consumer.start()
            self.is_connected = True
            logger.info(f"✅ Kafka consumer connected to {self.bootstrap_servers}, topics: {topics}")
        except Exception as e:
            logger.error(f"❌ Failed to connect Kafka consumer: {e}")
            self.is_connected = False
            raise
    
    async def stop(self):
        """Stop Kafka consumer"""
        if self.consumer:
            await self.consumer.stop()
            self.is_connected = False
            logger.info("✅ Kafka consumer stopped")
    
    async def consume(self):
        """Consume events from Kafka"""
        if not self.is_connected or not self.consumer:
            logger.warning("⚠️ Kafka consumer not connected")
            return None
        
        try:
            async for message in self.consumer:
                yield message.value
        except Exception as e:
            logger.error(f"❌ Error consuming from Kafka: {e}")


# Global Kafka publisher instance
_kafka_publisher: Optional[KafkaEventPublisher] = None


async def get_kafka_publisher() -> KafkaEventPublisher:
    """Get or create Kafka publisher instance"""
    global _kafka_publisher
    if _kafka_publisher is None:
        _kafka_publisher = KafkaEventPublisher()
        await _kafka_publisher.start()
    return _kafka_publisher


async def shutdown_kafka_publisher():
    """Shutdown Kafka publisher"""
    global _kafka_publisher
    if _kafka_publisher:
        await _kafka_publisher.stop()
        _kafka_publisher = None
