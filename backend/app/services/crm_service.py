"""CRM integration service for HubSpot and Salesforce."""
import httpx
from typing import Optional, Dict, Any, List
from app.config import settings
from app.models.lead import Lead


class HubSpotService:
    """Service for HubSpot CRM integration."""
    
    def __init__(self):
        self.api_key = settings.HUBSPOT_API_KEY
        self.base_url = "https://api.hubapi.com"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def create_contact(self, lead: Lead) -> Dict[str, Any]:
        """Create a contact in HubSpot from a lead."""
        contact_data = {
            "properties": {
                "email": lead.email or "",
                "phone": lead.phone,
                "firstname": lead.name.split()[0] if lead.name else "",
                "lastname": " ".join(lead.name.split()[1:]) if lead.name and len(lead.name.split()) > 1 else "",
                "company": lead.company or "",
                "hs_lead_status": lead.status.value if lead.status else "NEW",
                "lifecyclestage": "lead"
            }
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/crm/v3/objects/contacts",
                headers=self.headers,
                json=contact_data,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    async def update_contact(
        self,
        contact_id: str,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a contact in HubSpot."""
        contact_data = {
            "properties": updates
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.patch(
                f"{self.base_url}/crm/v3/objects/contacts/{contact_id}",
                headers=self.headers,
                json=contact_data,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    async def get_contact(self, contact_id: str) -> Dict[str, Any]:
        """Get a contact from HubSpot."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/crm/v3/objects/contacts/{contact_id}",
                headers=self.headers,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    async def search_contact_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Search for a contact by email."""
        search_data = {
            "filterGroups": [
                {
                    "filters": [
                        {
                            "propertyName": "email",
                            "operator": "EQ",
                            "value": email
                        }
                    ]
                }
            ],
            "limit": 1
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/crm/v3/objects/contacts/search",
                headers=self.headers,
                json=search_data,
                timeout=30.0
            )
            response.raise_for_status()
            results = response.json()
            if results.get("results"):
                return results["results"][0]
            return None
    
    async def create_note(
        self,
        contact_id: str,
        note_content: str
    ) -> Dict[str, Any]:
        """Create a note associated with a contact."""
        note_data = {
            "properties": {
                "hs_note_body": note_content,
                "hs_timestamp": None
            },
            "associations": [
                {
                    "to": {
                        "id": contact_id
                    },
                    "types": [
                        {
                            "associationCategory": "HUBSPOT_DEFINED",
                            "associationTypeId": 214
                        }
                    ]
                }
            ]
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/crm/v3/objects/notes",
                headers=self.headers,
                json=note_data,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    async def sync_lead_to_crm(self, lead: Lead) -> Optional[str]:
        """Sync a lead to HubSpot and return the CRM ID."""
        if not self.api_key:
            return None
        
        try:
            # Check if contact already exists
            if lead.email:
                existing = await self.search_contact_by_email(lead.email)
                if existing:
                    contact_id = existing["id"]
                    # Update existing contact
                    await self.update_contact(contact_id, {
                        "phone": lead.phone,
                        "hs_lead_status": lead.status.value if lead.status else "NEW"
                    })
                    return contact_id
            
            # Create new contact
            result = await self.create_contact(lead)
            return result.get("id")
        except Exception as e:
            print(f"Error syncing lead to HubSpot: {str(e)}")
            return None


class SalesforceService:
    """Service for Salesforce CRM integration."""
    
    def __init__(self):
        self.client_id = settings.SALESFORCE_CLIENT_ID
        self.client_secret = settings.SALESFORCE_CLIENT_SECRET
        self.username = settings.SALESFORCE_USERNAME
        self.password = settings.SALESFORCE_PASSWORD
        self.access_token: Optional[str] = None
        self.instance_url: Optional[str] = None
    
    async def authenticate(self) -> bool:
        """Authenticate with Salesforce and get access token."""
        if not all([self.client_id, self.client_secret, self.username, self.password]):
            return False
        
        auth_data = {
            "grant_type": "password",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "username": self.username,
            "password": self.password
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://login.salesforce.com/services/oauth2/token",
                data=auth_data,
                timeout=30.0
            )
            if response.status_code == 200:
                result = response.json()
                self.access_token = result.get("access_token")
                self.instance_url = result.get("instance_url")
                return True
            return False
    
    async def create_lead(self, lead: Lead) -> Optional[Dict[str, Any]]:
        """Create a lead in Salesforce."""
        if not self.access_token:
            if not await self.authenticate():
                return None
        
        lead_data = {
            "FirstName": lead.name.split()[0] if lead.name else "",
            "LastName": " ".join(lead.name.split()[1:]) if lead.name and len(lead.name.split()) > 1 else lead.name or "",
            "Email": lead.email or "",
            "Phone": lead.phone,
            "Company": lead.company or "",
            "Status": lead.status.value if lead.status else "New"
        }
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.instance_url}/services/data/v57.0/sobjects/Lead/",
                headers=headers,
                json=lead_data,
                timeout=30.0
            )
            if response.status_code in [200, 201]:
                return response.json()
            return None


class CRMService:
    """Unified CRM service that supports multiple providers."""
    
    def __init__(self):
        self.hubspot = HubSpotService() if settings.HUBSPOT_API_KEY else None
        self.salesforce = SalesforceService() if settings.SALESFORCE_CLIENT_ID else None
    
    async def sync_lead(self, lead: Lead, provider: str = "hubspot") -> Optional[str]:
        """Sync a lead to the specified CRM provider."""
        if provider.lower() == "hubspot" and self.hubspot:
            return await self.hubspot.sync_lead_to_crm(lead)
        elif provider.lower() == "salesforce" and self.salesforce:
            result = await self.salesforce.create_lead(lead)
            return result.get("id") if result else None
        return None

