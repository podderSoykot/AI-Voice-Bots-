"""Appointment model."""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.database.connection import Base


class AppointmentStatus(str, enum.Enum):
    """Appointment status enumeration."""
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    RESCHEDULED = "rescheduled"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    NO_SHOW = "no_show"


class Appointment(Base):
    """Appointment model for storing appointment information."""
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False, index=True)
    scheduled_time = Column(DateTime(timezone=True), nullable=False, index=True)
    status = Column(SQLEnum(AppointmentStatus), default=AppointmentStatus.SCHEDULED, nullable=False)
    calendar_event_id = Column(String(200), nullable=True, index=True)  # Google Calendar event ID
    notes = Column(String(1000), nullable=True)
    reminder_sent = Column(String(10), default="false", nullable=False)  # "true" or "false"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    lead = relationship("Lead", back_populates="appointments")

