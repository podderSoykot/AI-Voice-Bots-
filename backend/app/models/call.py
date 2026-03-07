"""Call model."""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.database.connection import Base


class CallStatus(str, enum.Enum):
    """Call status enumeration."""
    INITIATED = "initiated"
    RINGING = "ringing"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    NO_ANSWER = "no_answer"
    BUSY = "busy"


class CallOutcome(str, enum.Enum):
    """Call outcome enumeration."""
    SUCCESS = "success"
    APPOINTMENT_SET = "appointment_set"
    FOLLOW_UP_NEEDED = "follow_up_needed"
    NOT_INTERESTED = "not_interested"
    WRONG_NUMBER = "wrong_number"
    NO_ANSWER = "no_answer"


class Call(Base):
    """Call model for storing call records."""
    __tablename__ = "calls"
    
    id = Column(Integer, primary_key=True, index=True)
    call_id = Column(String(100), unique=True, nullable=False, index=True)  # Vapi call ID
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False, index=True)
    direction = Column(String(10), nullable=False)  # "inbound" or "outbound"
    status = Column(SQLEnum(CallStatus), default=CallStatus.INITIATED, nullable=False)
    outcome = Column(SQLEnum(CallOutcome), nullable=True)
    duration = Column(Integer, nullable=True)  # Duration in seconds
    transcript = Column(Text, nullable=True)
    recording_url = Column(String(500), nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    ended_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    lead = relationship("Lead", back_populates="calls")

