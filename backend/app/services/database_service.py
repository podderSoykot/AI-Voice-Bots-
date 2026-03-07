"""Database service layer for CRUD operations."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from typing import List, Optional
from datetime import datetime, timezone

from app.models.lead import Lead, LeadStatus
from app.models.call import Call, CallStatus, CallOutcome
from app.models.appointment import Appointment, AppointmentStatus
from app.schemas.lead import LeadCreate, LeadUpdate
from app.schemas.call import CallCreate, CallUpdate
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate


class DatabaseService:
    """Service for database operations."""
    
    @staticmethod
    async def create_lead(db: AsyncSession, lead_data: LeadCreate) -> Lead:
        """Create a new lead."""
        lead = Lead(**lead_data.model_dump())
        db.add(lead)
        await db.commit()
        await db.refresh(lead)
        return lead
    
    @staticmethod
    async def get_lead(db: AsyncSession, lead_id: int) -> Optional[Lead]:
        """Get a lead by ID."""
        result = await db.execute(
            select(Lead)
            .where(Lead.id == lead_id)
            .options(selectinload(Lead.calls), selectinload(Lead.appointments))
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_leads(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        status: Optional[LeadStatus] = None
    ) -> List[Lead]:
        """Get all leads with optional filtering."""
        query = select(Lead)
        if status:
            query = query.where(Lead.status == status)
        query = query.offset(skip).limit(limit).order_by(Lead.created_at.desc())
        result = await db.execute(query)
        return list(result.scalars().all())
    
    @staticmethod
    async def update_lead(
        db: AsyncSession,
        lead_id: int,
        lead_data: LeadUpdate
    ) -> Optional[Lead]:
        """Update a lead."""
        update_data = lead_data.model_dump(exclude_unset=True)
        if not update_data:
            return await DatabaseService.get_lead(db, lead_id)
        
        await db.execute(
            update(Lead)
            .where(Lead.id == lead_id)
            .values(**update_data, updated_at=datetime.now(timezone.utc))
        )
        await db.commit()
        return await DatabaseService.get_lead(db, lead_id)
    
    @staticmethod
    async def delete_lead(db: AsyncSession, lead_id: int) -> bool:
        """Delete a lead."""
        result = await db.execute(delete(Lead).where(Lead.id == lead_id))
        await db.commit()
        return result.rowcount > 0
    
    @staticmethod
    async def create_call(db: AsyncSession, call_data: CallCreate) -> Call:
        """Create a new call record."""
        call = Call(**call_data.model_dump())
        db.add(call)
        await db.commit()
        await db.refresh(call)
        return call
    
    @staticmethod
    async def get_call(db: AsyncSession, call_id: int) -> Optional[Call]:
        """Get a call by ID."""
        result = await db.execute(
            select(Call)
            .where(Call.id == call_id)
            .options(selectinload(Call.lead))
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_call_by_vapi_id(db: AsyncSession, vapi_call_id: str) -> Optional[Call]:
        """Get a call by Vapi call ID."""
        result = await db.execute(
            select(Call)
            .where(Call.call_id == vapi_call_id)
            .options(selectinload(Call.lead))
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_calls(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        lead_id: Optional[int] = None
    ) -> List[Call]:
        """Get all calls with optional filtering."""
        query = select(Call)
        if lead_id:
            query = query.where(Call.lead_id == lead_id)
        query = query.offset(skip).limit(limit).order_by(Call.created_at.desc())
        result = await db.execute(query)
        return list(result.scalars().all())
    
    @staticmethod
    async def update_call(
        db: AsyncSession,
        call_id: int,
        call_data: CallUpdate
    ) -> Optional[Call]:
        """Update a call record."""
        update_data = call_data.model_dump(exclude_unset=True)
        if not update_data:
            return await DatabaseService.get_call(db, call_id)
        
        await db.execute(
            update(Call)
            .where(Call.id == call_id)
            .values(**update_data, updated_at=datetime.now(timezone.utc))
        )
        await db.commit()
        return await DatabaseService.get_call(db, call_id)
    
    @staticmethod
    async def update_call_by_vapi_id(
        db: AsyncSession,
        vapi_call_id: str,
        call_data: CallUpdate
    ) -> Optional[Call]:
        """Update a call record by Vapi call ID."""
        update_data = call_data.model_dump(exclude_unset=True)
        if not update_data:
            return await DatabaseService.get_call_by_vapi_id(db, vapi_call_id)
        
        await db.execute(
            update(Call)
            .where(Call.call_id == vapi_call_id)
            .values(**update_data, updated_at=datetime.now(timezone.utc))
        )
        await db.commit()
        return await DatabaseService.get_call_by_vapi_id(db, vapi_call_id)
    
    @staticmethod
    async def create_appointment(
        db: AsyncSession,
        appointment_data: AppointmentCreate
    ) -> Appointment:
        """Create a new appointment."""
        appointment = Appointment(**appointment_data.model_dump())
        db.add(appointment)
        await db.commit()
        await db.refresh(appointment)
        return appointment
    
    @staticmethod
    async def get_appointment(
        db: AsyncSession,
        appointment_id: int
    ) -> Optional[Appointment]:
        """Get an appointment by ID."""
        result = await db.execute(
            select(Appointment)
            .where(Appointment.id == appointment_id)
            .options(selectinload(Appointment.lead))
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_appointments(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        lead_id: Optional[int] = None,
        status: Optional[AppointmentStatus] = None
    ) -> List[Appointment]:
        """Get all appointments with optional filtering."""
        query = select(Appointment)
        if lead_id:
            query = query.where(Appointment.lead_id == lead_id)
        if status:
            query = query.where(Appointment.status == status)
        query = query.offset(skip).limit(limit).order_by(Appointment.scheduled_time)
        result = await db.execute(query)
        return list(result.scalars().all())
    
    @staticmethod
    async def update_appointment(
        db: AsyncSession,
        appointment_id: int,
        appointment_data: AppointmentUpdate
    ) -> Optional[Appointment]:
        """Update an appointment."""
        update_data = appointment_data.model_dump(exclude_unset=True)
        if not update_data:
            return await DatabaseService.get_appointment(db, appointment_id)
        
        await db.execute(
            update(Appointment)
            .where(Appointment.id == appointment_id)
            .values(**update_data, updated_at=datetime.now(timezone.utc))
        )
        await db.commit()
        return await DatabaseService.get_appointment(db, appointment_id)
    
    @staticmethod
    async def delete_appointment(
        db: AsyncSession,
        appointment_id: int
    ) -> bool:
        """Delete an appointment."""
        result = await db.execute(
            delete(Appointment).where(Appointment.id == appointment_id)
        )
        await db.commit()
        return result.rowcount > 0

