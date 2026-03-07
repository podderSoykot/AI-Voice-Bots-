"""n8n workflow automation integration service."""
import httpx
from typing import Optional, Dict, Any
from app.config import settings


class N8nService:
    """Service for n8n workflow automation."""
    
    def __init__(self):
        self.webhook_url = settings.N8N_WEBHOOK_URL
        self.api_key = settings.N8N_API_KEY
        self.headers = {
            "Content-Type": "application/json"
        }
        
        if self.api_key:
            self.headers["X-N8N-API-KEY"] = self.api_key
    
    async def trigger_webhook(
        self,
        workflow_id: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """Trigger an n8n webhook workflow."""
        if not self.webhook_url:
            return None
        
        url = self.webhook_url
        if workflow_id:
            url = f"{url}/{workflow_id}"
        
        payload = data or {}
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    headers=self.headers,
                    json=payload,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json() if response.content else {"status": "success"}
        except Exception as e:
            print(f"Error triggering n8n webhook: {str(e)}")
            return None
    
    async def trigger_lead_qualified_workflow(
        self,
        lead_id: int,
        lead_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Trigger workflow when a lead is qualified."""
        return await self.trigger_webhook(
            data={
                "event": "lead_qualified",
                "lead_id": lead_id,
                "lead": lead_data
            }
        )
    
    async def trigger_appointment_set_workflow(
        self,
        appointment_id: int,
        appointment_data: Dict[str, Any],
        lead_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Trigger workflow when an appointment is set."""
        return await self.trigger_webhook(
            data={
                "event": "appointment_set",
                "appointment_id": appointment_id,
                "appointment": appointment_data,
                "lead": lead_data
            }
        )
    
    async def trigger_call_completed_workflow(
        self,
        call_id: int,
        call_data: Dict[str, Any],
        lead_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Trigger workflow when a call is completed."""
        return await self.trigger_webhook(
            data={
                "event": "call_completed",
                "call_id": call_id,
                "call": call_data,
                "lead": lead_data
            }
        )
    
    async def trigger_follow_up_workflow(
        self,
        lead_id: int,
        lead_data: Dict[str, Any],
        follow_up_type: str = "email"
    ) -> Optional[Dict[str, Any]]:
        """Trigger follow-up workflow for a lead."""
        return await self.trigger_webhook(
            data={
                "event": "follow_up",
                "lead_id": lead_id,
                "lead": lead_data,
                "follow_up_type": follow_up_type
            }
        )
    
    async def trigger_crm_sync_workflow(
        self,
        lead_id: int,
        lead_data: Dict[str, Any],
        crm_provider: str = "hubspot"
    ) -> Optional[Dict[str, Any]]:
        """Trigger CRM sync workflow."""
        return await self.trigger_webhook(
            data={
                "event": "crm_sync",
                "lead_id": lead_id,
                "lead": lead_data,
                "crm_provider": crm_provider
            }
        )

