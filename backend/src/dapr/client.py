"""
Dapr Client for Phase 5 Cloud-Native Integration
"""

import json
import httpx
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)


class DaprClient:
    """Dapr client for cloud-native service communication"""
    
    def __init__(self, dapr_port: int = 3500, dapr_host: str = "localhost"):
        self.dapr_port = dapr_port
        self.dapr_host = dapr_host
        self.base_url = f"http://{dapr_host}:{dapr_port}"
        
    async def publish_event(self, pubsub_name: str, topic: str, data: Dict[str, Any]) -> bool:
        """Publish event via Dapr pub/sub"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/v1.0/publish/{pubsub_name}/{topic}",
                    json=data,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    logger.info(f"Published event to {topic} via Dapr")
                    return True
                else:
                    logger.error(f"Failed to publish event: {response.status_code} - {response.text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error publishing event via Dapr: {e}")
            return False
    
    async def get_state(self, store_name: str, key: str) -> Optional[Dict[str, Any]]:
        """Get state from Dapr state store"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/v1.0/state/{store_name}/{key}"
                )
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 204:
                    return None
                else:
                    logger.error(f"Failed to get state: {response.status_code}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error getting state via Dapr: {e}")
            return None
    
    async def save_state(self, store_name: str, key: str, value: Dict[str, Any]) -> bool:
        """Save state to Dapr state store"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/v1.0/state/{store_name}",
                    json=[{
                        "key": key,
                        "value": value
                    }],
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 204:
                    logger.info(f"Saved state for key {key}")
                    return True
                else:
                    logger.error(f"Failed to save state: {response.status_code}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error saving state via Dapr: {e}")
            return False
    
    async def delete_state(self, store_name: str, key: str) -> bool:
        """Delete state from Dapr state store"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(
                    f"{self.base_url}/v1.0/state/{store_name}/{key}"
                )
                
                if response.status_code == 204:
                    logger.info(f"Deleted state for key {key}")
                    return True
                else:
                    logger.error(f"Failed to delete state: {response.status_code}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error deleting state via Dapr: {e}")
            return False
    
    async def invoke_service(self, app_id: str, method: str, data: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Invoke another service via Dapr service invocation"""
        try:
            async with httpx.AsyncClient() as client:
                url = f"{self.base_url}/v1.0/invoke/{app_id}/method/{method}"
                
                if data:
                    response = await client.post(url, json=data)
                else:
                    response = await client.get(url)
                
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.error(f"Service invocation failed: {response.status_code}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error invoking service via Dapr: {e}")
            return None
    
    async def get_secret(self, secret_store: str, key: str) -> Optional[str]:
        """Get secret from Dapr secret store"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/v1.0/secrets/{secret_store}/{key}"
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get(key)
                else:
                    logger.error(f"Failed to get secret: {response.status_code}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error getting secret via Dapr: {e}")
            return None
    
    async def schedule_job(self, job_name: str, schedule: str, data: Dict[str, Any]) -> bool:
        """Schedule a job using Dapr Jobs API"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/v1.0-alpha1/jobs/{job_name}",
                    json={
                        "dueTime": schedule,
                        "data": data
                    }
                )

                if response.status_code in [200, 201]:
                    logger.info(f"Scheduled job {job_name}")
                    return True
                else:
                    logger.error(f"Failed to schedule job: {response.status_code} - {response.text}")
                    return False

        except Exception as e:
            logger.error(f"Error scheduling job via Dapr: {e}")
            return False

    async def trigger_job(self, job_name: str, data: Dict[str, Any]) -> bool:
        """Trigger a job immediately using Dapr Jobs API"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/v1.0-alpha1/jobs/{job_name}/trigger",
                    json={"data": data}
                )

                if response.status_code == 200:
                    logger.info(f"Triggered job {job_name}")
                    return True
                else:
                    logger.error(f"Failed to trigger job: {response.status_code}")
                    return False

        except Exception as e:
            logger.error(f"Error triggering job via Dapr: {e}")
            return False

    async def delete_job(self, job_name: str) -> bool:
        """Delete a scheduled job using Dapr Jobs API"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(
                    f"{self.base_url}/v1.0-alpha1/jobs/{job_name}"
                )

                if response.status_code == 204:
                    logger.info(f"Deleted job {job_name}")
                    return True
                else:
                    logger.error(f"Failed to delete job: {response.status_code}")
                    return False

        except Exception as e:
            logger.error(f"Error deleting job via Dapr: {e}")
            return False


# Global Dapr client instance
_dapr_client: Optional[DaprClient] = None


def get_dapr_client() -> DaprClient:
    """Get or create the global Dapr client"""
    global _dapr_client
    if _dapr_client is None:
        _dapr_client = DaprClient()
    return _dapr_client


class DaprEventPublisher:
    """Event publisher using Dapr pub/sub"""
    
    def __init__(self, pubsub_name: str = "kafka-pubsub"):
        self.pubsub_name = pubsub_name
        self.dapr_client = get_dapr_client()
    
    async def publish_task_created(self, task_id: int, user_id: str, task_data: Dict[str, Any]) -> bool:
        """Publish task created event via Dapr"""
        event_data = {
            "event_id": f"task-created-{task_id}",
            "event_type": "task.created",
            "aggregate_id": str(task_id),
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat(),
            "data": {
                "task_id": task_id,
                "title": task_data.get("title"),
                "description": task_data.get("description"),
                "priority": task_data.get("priority", "medium"),
                "category": task_data.get("category", "General"),
                "tags": task_data.get("tags", []),
                "due_date": task_data.get("due_date"),
                "user_id": user_id
            }
        }
        
        return await self.dapr_client.publish_event(
            self.pubsub_name, 
            "task-events", 
            event_data
        )
    
    async def publish_task_completed(self, task_id: int, user_id: str, task_data: Dict[str, Any]) -> bool:
        """Publish task completed event via Dapr"""
        event_data = {
            "event_id": f"task-completed-{task_id}",
            "event_type": "task.completed",
            "aggregate_id": str(task_id),
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat(),
            "data": {
                "task_id": task_id,
                "title": task_data.get("title"),
                "completed_at": task_data.get("completed_at"),
                "was_overdue": task_data.get("was_overdue", False),
                "user_id": user_id
            }
        }
        
        return await self.dapr_client.publish_event(
            self.pubsub_name, 
            "task-events", 
            event_data
        )
    
    async def publish_reminder_due(self, reminder_id: int, task_id: int, user_id: str, message: str) -> bool:
        """Publish reminder due event via Dapr"""
        event_data = {
            "event_id": f"reminder-{reminder_id}",
            "event_type": "reminder.triggered",
            "aggregate_id": str(reminder_id),
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat(),
            "data": {
                "reminder_id": reminder_id,
                "task_id": task_id,
                "user_id": user_id,
                "message": message,
                "triggered_at": datetime.utcnow().isoformat()
            }
        }

        return await self.dapr_client.publish_event(
            self.pubsub_name,
            "reminders",
            event_data
        )

    async def schedule_reminder_job(self, reminder_id: int, remind_at: datetime, task_id: int, user_id: str, message: str) -> bool:
        """Schedule a reminder job using Dapr Jobs API for exact timing"""
        job_name = f"reminder-{reminder_id}-{task_id}"
        
        # Format the datetime for Dapr Jobs API (ISO format)
        schedule_time = remind_at.isoformat()
        
        job_data = {
            "reminder_id": reminder_id,
            "task_id": task_id,
            "user_id": user_id,
            "message": message,
            "scheduled_at": datetime.utcnow().isoformat(),
            "remind_at": remind_at.isoformat()
        }

        return await self.dapr_client.schedule_job(
            job_name=job_name,
            schedule=schedule_time,
            data=job_data
        )