"""Appointment Pydantic schemas."""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.appointment import AppointmentStatus


class AppointmentBase(BaseModel):
    """Base appointment schema."""
    scheduled_time: datetime
    notes: Optional[str] = Field(None, max_length=1000)


class AppointmentCreate(AppointmentBase):
    """Schema for creating an appointment."""
    lead_id: int


class AppointmentUpdate(BaseModel):
    """Schema for updating an appointment."""
    scheduled_time: Optional[datetime] = None
    status: Optional[AppointmentStatus] = None
    notes: Optional[str] = Field(None, max_length=1000)
    calendar_event_id: Optional[str] = Field(None, max_length=200)


class AppointmentResponse(AppointmentBase):
    """Schema for appointment response."""
    id: int
    lead_id: int
    status: AppointmentStatus
    calendar_event_id: Optional[str]
    reminder_sent: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

