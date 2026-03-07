"""Call Pydantic schemas."""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.call import CallStatus, CallOutcome


class CallInitiate(BaseModel):
    """Schema for initiating a call."""
    lead_id: int
    phone_number: Optional[str] = None  # Override lead's phone if provided


class CallCreate(BaseModel):
    """Schema for creating a call record."""
    call_id: str = Field(..., max_length=100)
    lead_id: int
    direction: str = Field(..., pattern="^(inbound|outbound)$")


class CallUpdate(BaseModel):
    """Schema for updating a call record."""
    status: Optional[CallStatus] = None
    outcome: Optional[CallOutcome] = None
    duration: Optional[int] = None
    transcript: Optional[str] = None
    recording_url: Optional[str] = Field(None, max_length=500)
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None


class CallResponse(BaseModel):
    """Schema for call response."""
    id: int
    call_id: str
    lead_id: int
    direction: str
    status: CallStatus
    outcome: Optional[CallOutcome]
    duration: Optional[int]
    transcript: Optional[str]
    recording_url: Optional[str]
    started_at: Optional[datetime]
    ended_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

