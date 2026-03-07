"""Lead model."""
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.database.connection import Base


class LeadStatus(str, enum.Enum):
    """Lead status enumeration."""
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    APPOINTMENT_SET = "appointment_set"
    CONVERTED = "converted"
    LOST = "lost"


class Lead(Base):
    """Lead model for storing lead information."""
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), nullable=True, index=True)
    phone = Column(String(20), nullable=False, index=True)
    company = Column(String(255), nullable=True)
    status = Column(SQLEnum(LeadStatus), default=LeadStatus.NEW, nullable=False)
    source = Column(String(100), nullable=True)
    notes = Column(String(1000), nullable=True)
    crm_id = Column(String(100), nullable=True, index=True)  # CRM system ID
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    calls = relationship("Call", back_populates="lead", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="lead", cascade="all, delete-orphan")

