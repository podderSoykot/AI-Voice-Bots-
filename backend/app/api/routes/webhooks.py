"""Webhook handlers for external services."""
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
import json

from app.database.connection import get_db
from app.services.database_service import DatabaseService
from app.services.n8n_service import N8nService
from app.models.call import CallStatus, CallOutcome
from app.utils.helpers import build_response

router = APIRouter()
n8n_service = N8nService()


@router.post("/webhooks/vapi", response_model=dict)
async def vapi_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Handle webhooks from Vapi."""
    try:
        payload = await request.json()
        event_type = payload.get("type")
        call_data = payload.get("call", {})
        call_id = call_data.get("id")
        
        if not call_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing call ID in webhook payload"
            )
        
        # Find or create call record
        call = await DatabaseService.get_call_by_vapi_id(db, call_id)
        
        if not call:
            # Try to get lead_id from metadata
            metadata = call_data.get("metadata", {})
            lead_id = metadata.get("lead_id")
            
            if not lead_id:
                # Return success but don't process
                return build_response(None, "Webhook received but no matching call record")
            
            # Create call record
            from app.schemas.call import CallCreate
            call = await DatabaseService.create_call(
                db,
                CallCreate(
                    call_id=call_id,
                    lead_id=lead_id,
                    direction=call_data.get("direction", "outbound")
                )
            )
        
        # Update call based on event type
        from app.schemas.call import CallUpdate
        from datetime import datetime, timezone
        
        update_data = {}
        
        if event_type == "call-status-update":
            status_mapping = {
                "ringing": CallStatus.RINGING,
                "in-progress": CallStatus.IN_PROGRESS,
                "ended": CallStatus.COMPLETED,
                "failed": CallStatus.FAILED,
                "no-answer": CallStatus.NO_ANSWER,
                "busy": CallStatus.BUSY
            }
            new_status = call_data.get("status", "").lower().replace("_", "-")
            if new_status in status_mapping:
                update_data["status"] = status_mapping[new_status]
        
        elif event_type == "call-end":
            update_data["status"] = CallStatus.COMPLETED
            update_data["ended_at"] = datetime.now(timezone.utc)
            
            # Calculate duration if available
            if call_data.get("duration"):
                update_data["duration"] = call_data.get("duration")
        
        elif event_type == "transcript":
            transcript_data = payload.get("transcript", {})
            if transcript_data:
                transcript_text = transcript_data.get("text", "")
                if transcript_text:
                    update_data["transcript"] = transcript_text
        
        elif event_type == "recording":
            recording_url = call_data.get("recordingUrl")
            if recording_url:
                update_data["recording_url"] = recording_url
        
        # Update call record
        if update_data:
            await DatabaseService.update_call_by_vapi_id(
                db,
                call_id,
                CallUpdate(**update_data)
            )
        
        # Trigger n8n workflow if call is completed
        if event_type == "call-end" and call:
            lead = await DatabaseService.get_lead(db, call.lead_id)
            if lead:
                await n8n_service.trigger_call_completed_workflow(
                    call_id=call.id,
                    call_data={
                        "call_id": call.call_id,
                        "duration": call.duration,
                        "transcript": call.transcript
                    },
                    lead_data={
                        "id": lead.id,
                        "name": lead.name,
                        "email": lead.email,
                        "phone": lead.phone
                    }
                )
        
        return build_response(None, "Webhook processed successfully")
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing webhook: {str(e)}"
        )


@router.post("/webhooks/crm", response_model=dict)
async def crm_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Handle webhooks from CRM systems."""
    try:
        payload = await request.json()
        # Process CRM webhook based on provider
        # This is a placeholder - implement based on your CRM provider's webhook format
        
        return build_response(None, "CRM webhook processed successfully")
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing CRM webhook: {str(e)}"
        )


@router.post("/webhooks/calendar", response_model=dict)
async def calendar_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Handle webhooks from calendar systems."""
    try:
        payload = await request.json()
        # Process calendar webhook
        # This is a placeholder - implement based on your calendar provider's webhook format
        
        return build_response(None, "Calendar webhook processed successfully")
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing calendar webhook: {str(e)}"
        )


@router.post("/webhooks/n8n", response_model=dict)
async def n8n_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Handle incoming webhooks from n8n workflows."""
    try:
        payload = await request.json()
        # Process n8n webhook data
        # This allows n8n workflows to trigger actions in the API
        
        return build_response(None, "n8n webhook processed successfully")
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing n8n webhook: {str(e)}"
        )

