"""Call management API routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.database.connection import get_db
from app.schemas.call import CallInitiate, CallResponse, CallUpdate
from app.services.database_service import DatabaseService
from app.services.vapi_service import VapiService
from app.utils.helpers import build_response

router = APIRouter()
vapi_service = VapiService()


@router.post("/calls/initiate", response_model=dict, status_code=status.HTTP_201_CREATED)
async def initiate_call(
    call_data: CallInitiate,
    assistant_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Initiate an outbound call using Vapi."""
    try:
        # Get lead information
        lead = await DatabaseService.get_lead(db, call_data.lead_id)
        if not lead:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Lead with ID {call_data.lead_id} not found"
            )
        
        # Use provided phone number or lead's phone
        phone_number = call_data.phone_number or lead.phone
        
        # Initiate call via Vapi
        vapi_response = await vapi_service.initiate_call(
            phone_number=phone_number,
            assistant_id=assistant_id,
            customer={
                "number": phone_number,
                "name": lead.name
            },
            metadata={
                "lead_id": lead.id,
                "lead_name": lead.name
            }
        )
        
        # Create call record in database
        from app.schemas.call import CallCreate
        call_record = await DatabaseService.create_call(
            db,
            CallCreate(
                call_id=vapi_response.get("id", ""),
                lead_id=lead.id,
                direction="outbound"
            )
        )
        
        return build_response(
            {
                "call": CallResponse.model_validate(call_record).model_dump(),
                "vapi_response": vapi_response
            },
            "Call initiated successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error initiating call: {str(e)}"
        )


@router.get("/calls", response_model=dict)
async def get_calls(
    skip: int = 0,
    limit: int = 100,
    lead_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all calls with optional filtering."""
    try:
        calls = await DatabaseService.get_calls(db, skip, limit, lead_id)
        return build_response(
            [CallResponse.model_validate(call).model_dump() for call in calls],
            "Calls retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving calls: {str(e)}"
        )


@router.get("/calls/{call_id}", response_model=dict)
async def get_call(
    call_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific call by ID."""
    try:
        call = await DatabaseService.get_call(db, call_id)
        if not call:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Call with ID {call_id} not found"
            )
        
        return build_response(
            CallResponse.model_validate(call).model_dump(),
            "Call retrieved successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving call: {str(e)}"
        )


@router.get("/calls/vapi/{vapi_call_id}", response_model=dict)
async def get_call_by_vapi_id(
    vapi_call_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get a call by Vapi call ID."""
    try:
        call = await DatabaseService.get_call_by_vapi_id(db, vapi_call_id)
        if not call:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Call with Vapi ID {vapi_call_id} not found"
            )
        
        return build_response(
            CallResponse.model_validate(call).model_dump(),
            "Call retrieved successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving call: {str(e)}"
        )


@router.put("/calls/{call_id}", response_model=dict)
async def update_call(
    call_id: int,
    call_data: CallUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a call record."""
    try:
        call = await DatabaseService.get_call(db, call_id)
        if not call:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Call with ID {call_id} not found"
            )
        
        updated_call = await DatabaseService.update_call(db, call_id, call_data)
        
        return build_response(
            CallResponse.model_validate(updated_call).model_dump(),
            "Call updated successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating call: {str(e)}"
        )


@router.get("/calls/lead/{lead_id}", response_model=dict)
async def get_lead_calls(
    lead_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all calls for a specific lead."""
    try:
        calls = await DatabaseService.get_calls(db, lead_id=lead_id)
        return build_response(
            [CallResponse.model_validate(call).model_dump() for call in calls],
            "Lead calls retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving lead calls: {str(e)}"
        )

