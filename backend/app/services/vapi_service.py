"""Vapi API integration service."""
import httpx
from typing import Optional, Dict, Any
from app.config import settings


class VapiService:
    """Service for interacting with Vapi API."""
    
    def __init__(self):
        self.api_key = settings.VAPI_API_KEY
        self.base_url = settings.VAPI_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def create_agent(
        self,
        name: str,
        first_message: str,
        model: Optional[Dict[str, Any]] = None,
        voice: Optional[str] = None,
        language: Optional[str] = "en",
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Create a new Vapi agent."""
        default_model = {
            "provider": "openai",
            "model": "gpt-3.5-turbo",
            "temperature": 0.7,
            "maxTokens": 300
        }
        
        agent_data = {
            "name": name,
            "firstMessage": first_message,
            "model": model or default_model,
            "voice": voice or "jennifer-playht",
            "language": language,
            **kwargs
        }
        
        if system_prompt:
            agent_data["systemPrompt"] = system_prompt
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/assistant",
                headers=self.headers,
                json=agent_data,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    async def get_agent(self, agent_id: str) -> Dict[str, Any]:
        """Get agent details by ID."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/assistant/{agent_id}",
                headers=self.headers,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    async def update_agent(
        self,
        agent_id: str,
        **updates
    ) -> Dict[str, Any]:
        """Update an existing agent."""
        async with httpx.AsyncClient() as client:
            response = await client.patch(
                f"{self.base_url}/assistant/{agent_id}",
                headers=self.headers,
                json=updates,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    async def initiate_call(
        self,
        phone_number: str,
        assistant_id: Optional[str] = None,
        assistant: Optional[Dict[str, Any]] = None,
        customer: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Initiate an outbound call."""
        call_data = {
            "phoneNumberId": phone_number,  # This should be a phone number ID from Vapi
            **kwargs
        }
        
        if assistant_id:
            call_data["assistantId"] = assistant_id
        elif assistant:
            call_data["assistant"] = assistant
        
        if customer:
            call_data["customer"] = customer
        
        if metadata:
            call_data["metadata"] = metadata
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/call",
                headers=self.headers,
                json=call_data,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    async def get_call(self, call_id: str) -> Dict[str, Any]:
        """Get call details by ID."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/call/{call_id}",
                headers=self.headers,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    async def end_call(self, call_id: str) -> Dict[str, Any]:
        """End an active call."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/call/{call_id}/end",
                headers=self.headers,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    async def get_phone_numbers(self) -> Dict[str, Any]:
        """Get available phone numbers."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/phone-number",
                headers=self.headers,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    async def create_sales_agent(
        self,
        name: str = "Sales Agent",
        company_name: Optional[str] = None,
        product_description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a pre-configured sales agent."""
        system_prompt = f"""You are a professional sales representative for {company_name or 'our company'}.
Your goal is to:
1. Introduce yourself and the company
2. Qualify the lead by understanding their needs
3. Present our {product_description or 'products/services'} if relevant
4. Schedule an appointment if the lead is interested
5. Be polite, professional, and concise

Keep the conversation natural and engaging. If the lead is not interested, thank them for their time and end the call gracefully."""
        
        first_message = f"Hi! This is {name} calling from {company_name or 'our company'}. Do you have a moment to talk?"
        
        return await self.create_agent(
            name=name,
            first_message=first_message,
            system_prompt=system_prompt,
            voice="jennifer-playht",
            language="en"
        )

