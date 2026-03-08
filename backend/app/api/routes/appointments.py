"""Appointment management API routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database.connection import get_db
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate, AppointmentResponse
from app.models.appointment import AppointmentStatus
from app.services.database_service import DatabaseService
from app.services.calendar_service import GoogleCalendarService
from app.utils.helpers import build_response

router = APIRouter()
calendar_service = GoogleCalendarService()


@router.post("/appointments", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_appointment(
    appointment_data: AppointmentCreate,
    create_calendar_event: bool = True,
    db: AsyncSession = Depends(get_db)
):
    """Create a new appointment."""
    try:
        # Verify lead exists
        lead = await DatabaseService.get_lead(db, appointment_data.lead_id)
        if not lead:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Lead with ID {appointment_data.lead_id} not found"
            )
        
        # Create appointment
        appointment = await DatabaseService.create_appointment(db, appointment_data)
        
        # Create calendar event if requested
        calendar_event_id = None
        if create_calendar_event and calendar_service.service:
            calendar_event_id = calendar_service.create_appointment_event(
                appointment=appointment,
                lead=lead
            )
            
            if calendar_event_id:
                # Update appointment with calendar event ID
                appointment = await DatabaseService.update_appointment(
                    db,
                    appointment.id,
                    AppointmentUpdate(calendar_event_id=calendar_event_id)
                )
        
        return build_response(
            AppointmentResponse.model_validate(appointment).model_dump(),
            "Appointment created successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating appointment: {str(e)}"
        )


@router.get("/appointments", response_model=dict)
async def get_appointments(
    skip: int = 0,
    limit: int = 100,
    lead_id: Optional[int] = None,
    status_filter: Optional[AppointmentStatus] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all appointments with optional filtering."""
    try:
        appointments = await DatabaseService.get_appointments(
            db, skip, limit, lead_id, status_filter
        )
        return build_response(
            [AppointmentResponse.model_validate(apt).model_dump() for apt in appointments],
            "Appointments retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving appointments: {str(e)}"
        )


@router.get("/appointments/{appointment_id}", response_model=dict)
async def get_appointment(
    appointment_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific appointment by ID."""
    try:
        appointment = await DatabaseService.get_appointment(db, appointment_id)
        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Appointment with ID {appointment_id} not found"
            )
        
        return build_response(
            AppointmentResponse.model_validate(appointment).model_dump(),
            "Appointment retrieved successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving appointment: {str(e)}"
        )


@router.put("/appointments/{appointment_id}", response_model=dict)
async def update_appointment(
    appointment_id: int,
    appointment_data: AppointmentUpdate,
    update_calendar: bool = True,
    db: AsyncSession = Depends(get_db)
):
    """Update an appointment."""
    try:
        appointment = await DatabaseService.get_appointment(db, appointment_id)
        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Appointment with ID {appointment_id} not found"
            )
        
        # Update appointment
        updated_appointment = await DatabaseService.update_appointment(
            db, appointment_id, appointment_data
        )
        
        # Update calendar event if requested and event exists
        if update_calendar and updated_appointment.calendar_event_id and calendar_service.service:
            lead = await DatabaseService.get_lead(db, updated_appointment.lead_id)
            if lead:
                calendar_service.update_event(
                    event_id=updated_appointment.calendar_event_id,
                    appointment=updated_appointment,
                    lead=lead
                )
        
        return build_response(
            AppointmentResponse.model_validate(updated_appointment).model_dump(),
            "Appointment updated successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating appointment: {str(e)}"
        )


@router.delete("/appointments/{appointment_id}", response_model=dict)
async def delete_appointment(
    appointment_id: int,
    delete_calendar_event: bool = True,
    db: AsyncSession = Depends(get_db)
):
    """Delete an appointment."""
    try:
        appointment = await DatabaseService.get_appointment(db, appointment_id)
        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Appointment with ID {appointment_id} not found"
            )
        
        # Delete calendar event if requested
        if delete_calendar_event and appointment.calendar_event_id and calendar_service.service:
            calendar_service.delete_event(appointment.calendar_event_id)
        
        # Delete appointment
        success = await DatabaseService.delete_appointment(db, appointment_id)
        
        return build_response(None, "Appointment deleted successfully")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting appointment: {str(e)}"
        )


@router.get("/appointments/lead/{lead_id}", response_model=dict)
async def get_lead_appointments(
    lead_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all appointments for a specific lead."""
    try:
        appointments = await DatabaseService.get_appointments(db, lead_id=lead_id)
        return build_response(
            [AppointmentResponse.model_validate(apt).model_dump() for apt in appointments],
            "Lead appointments retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving lead appointments: {str(e)}"
        )

