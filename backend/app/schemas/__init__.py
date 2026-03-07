"""Pydantic schemas for API validation."""
from app.schemas.lead import LeadCreate, LeadUpdate, LeadResponse
from app.schemas.call import CallCreate, CallResponse, CallInitiate
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate, AppointmentResponse

__all__ = [
    "LeadCreate", "LeadUpdate", "LeadResponse",
    "CallCreate", "CallResponse", "CallInitiate",
    "AppointmentCreate", "AppointmentUpdate", "AppointmentResponse"
]

