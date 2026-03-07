"""Lead Pydantic schemas."""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.models.lead import LeadStatus


class LeadBase(BaseModel):
    """Base lead schema."""
    name: str = Field(..., min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    phone: str = Field(..., min_length=10, max_length=20)
    company: Optional[str] = Field(None, max_length=255)
    source: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = Field(None, max_length=1000)


class LeadCreate(LeadBase):
    """Schema for creating a lead."""
    pass


class LeadUpdate(BaseModel):
    """Schema for updating a lead."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=10, max_length=20)
    company: Optional[str] = Field(None, max_length=255)
    status: Optional[LeadStatus] = None
    source: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = Field(None, max_length=1000)
    crm_id: Optional[str] = Field(None, max_length=100)


class LeadResponse(LeadBase):
    """Schema for lead response."""
    id: int
    status: LeadStatus
    crm_id: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class LeadBulkCreate(BaseModel):
    """Schema for bulk creating leads."""
    leads: list[LeadCreate]

