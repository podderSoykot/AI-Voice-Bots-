"""Google Calendar integration service."""
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import json
import os
from app.config import settings
from app.models.appointment import Appointment
from app.models.lead import Lead


class GoogleCalendarService:
    """Service for Google Calendar integration."""
    
    def __init__(self):
        self.credentials_path = settings.GOOGLE_CALENDAR_CREDENTIALS
        self.calendar_id = settings.GOOGLE_CALENDAR_ID or "primary"
        self.service: Optional[Any] = None
        self._initialize_service()
    
    def _initialize_service(self):
        """Initialize Google Calendar service."""
        if not self.credentials_path or not os.path.exists(self.credentials_path):
            return
        
        try:
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path,
                scopes=['https://www.googleapis.com/auth/calendar']
            )
            self.service = build('calendar', 'v3', credentials=credentials)
        except Exception as e:
            print(f"Error initializing Google Calendar service: {str(e)}")
            self.service = None
    
    async def create_event(
        self,
        appointment: Appointment,
        lead: Lead,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        location: Optional[str] = None,
        duration_minutes: int = 30
    ) -> Optional[Dict[str, Any]]:
        """Create a calendar event for an appointment."""
        if not self.service:
            return None
        
        start_time = appointment.scheduled_time
        end_time = start_time + timedelta(minutes=duration_minutes)
        
        event_summary = summary or f"Appointment with {lead.name}"
        event_description = description or f"""
Appointment scheduled with {lead.name}
Phone: {lead.phone}
Email: {lead.email or 'N/A'}
Company: {lead.company or 'N/A'}

Notes: {appointment.notes or 'None'}
        """.strip()
        
        event = {
            'summary': event_summary,
            'description': event_description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'UTC',
            },
            'attendees': [
                {'email': lead.email} if lead.email else None
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},  # 1 day before
                    {'method': 'popup', 'minutes': 15},  # 15 minutes before
                ],
            },
        }
        
        # Remove None attendees
        event['attendees'] = [a for a in event['attendees'] if a is not None]
        
        if location:
            event['location'] = location
        
        try:
            created_event = self.service.events().insert(
                calendarId=self.calendar_id,
                body=event,
                sendUpdates='all' if lead.email else 'none'
            ).execute()
            
            return {
                'id': created_event.get('id'),
                'htmlLink': created_event.get('htmlLink'),
                'start': created_event.get('start'),
                'end': created_event.get('end')
            }
        except HttpError as e:
            print(f"Error creating calendar event: {str(e)}")
            return None
    
    async def update_event(
        self,
        event_id: str,
        appointment: Appointment,
        lead: Lead,
        summary: Optional[str] = None,
        description: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Update an existing calendar event."""
        if not self.service:
            return None
        
        try:
            # Get existing event
            event = self.service.events().get(
                calendarId=self.calendar_id,
                eventId=event_id
            ).execute()
            
            # Update event
            start_time = appointment.scheduled_time
            end_time = start_time + timedelta(minutes=30)
            
            event['summary'] = summary or event.get('summary', f"Appointment with {lead.name}")
            event['description'] = description or event.get('description', '')
            event['start']['dateTime'] = start_time.isoformat()
            event['end']['dateTime'] = end_time.isoformat()
            
            updated_event = self.service.events().update(
                calendarId=self.calendar_id,
                eventId=event_id,
                body=event,
                sendUpdates='all'
            ).execute()
            
            return {
                'id': updated_event.get('id'),
                'htmlLink': updated_event.get('htmlLink')
            }
        except HttpError as e:
            print(f"Error updating calendar event: {str(e)}")
            return None
    
    async def delete_event(self, event_id: str) -> bool:
        """Delete a calendar event."""
        if not self.service:
            return False
        
        try:
            self.service.events().delete(
                calendarId=self.calendar_id,
                eventId=event_id
            ).execute()
            return True
        except HttpError as e:
            print(f"Error deleting calendar event: {str(e)}")
            return False
    
    async def get_event(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Get a calendar event by ID."""
        if not self.service:
            return None
        
        try:
            event = self.service.events().get(
                calendarId=self.calendar_id,
                eventId=event_id
            ).execute()
            return event
        except HttpError as e:
            print(f"Error getting calendar event: {str(e)}")
            return None
    
    async def list_events(
        self,
        time_min: Optional[datetime] = None,
        time_max: Optional[datetime] = None,
        max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """List calendar events."""
        if not self.service:
            return []
        
        try:
            time_min = time_min or datetime.utcnow()
            time_max = time_max or time_min + timedelta(days=30)
            
            events_result = self.service.events().list(
                calendarId=self.calendar_id,
                timeMin=time_min.isoformat() + 'Z',
                timeMax=time_max.isoformat() + 'Z',
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            return events_result.get('items', [])
        except HttpError as e:
            print(f"Error listing calendar events: {str(e)}")
            return []
    
    async def create_appointment_event(
        self,
        appointment: Appointment,
        lead: Lead
    ) -> Optional[str]:
        """Create a calendar event for an appointment and return the event ID."""
        result = await self.create_event(
            appointment=appointment,
            lead=lead,
            summary=f"Sales Appointment - {lead.name}",
            description=f"""
Sales appointment scheduled with {lead.name}.

Contact Information:
- Phone: {lead.phone}
- Email: {lead.email or 'N/A'}
- Company: {lead.company or 'N/A'}

Appointment Notes:
{appointment.notes or 'None'}
            """.strip()
        )
        
        return result.get('id') if result else None

