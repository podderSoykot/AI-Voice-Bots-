"""Lead management API routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.database.connection import get_db
from app.schemas.lead import LeadCreate, LeadUpdate, LeadResponse, LeadBulkCreate
from app.models.lead import LeadStatus
from app.services.database_service import DatabaseService
from app.services.crm_service import CRMService
from app.utils.helpers import build_response, build_error_response

router = APIRouter()
crm_service = CRMService()


@router.post("/leads", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_lead(
    lead_data: LeadCreate,
    db: AsyncSession = Depends(get_db),
    sync_crm: bool = False
):
    """Create a new lead."""
    try:
        lead = await DatabaseService.create_lead(db, lead_data)
        
        # Optionally sync to CRM
        if sync_crm:
            crm_id = await crm_service.sync_lead(lead, provider="hubspot")
            if crm_id:
                await DatabaseService.update_lead(
                    db,
                    lead.id,
                    LeadUpdate(crm_id=crm_id)
                )
                lead.crm_id = crm_id
        
        return build_response(
            LeadResponse.model_validate(lead).model_dump(),
            "Lead created successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating lead: {str(e)}"
        )


@router.post("/leads/bulk", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_leads_bulk(
    bulk_data: LeadBulkCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create multiple leads at once."""
    try:
        created_leads = []
        for lead_data in bulk_data.leads:
            lead = await DatabaseService.create_lead(db, lead_data)
            created_leads.append(LeadResponse.model_validate(lead).model_dump())
        
        return build_response(
            {"leads": created_leads, "count": len(created_leads)},
            f"Successfully created {len(created_leads)} leads"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating leads: {str(e)}"
        )


@router.get("/leads", response_model=dict)
async def get_leads(
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[LeadStatus] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all leads with optional filtering."""
    try:
        leads = await DatabaseService.get_leads(db, skip, limit, status_filter)
        return build_response(
            [LeadResponse.model_validate(lead).model_dump() for lead in leads],
            "Leads retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving leads: {str(e)}"
        )


@router.get("/leads/{lead_id}", response_model=dict)
async def get_lead(
    lead_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific lead by ID."""
    try:
        lead = await DatabaseService.get_lead(db, lead_id)
        if not lead:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Lead with ID {lead_id} not found"
            )
        
        return build_response(
            LeadResponse.model_validate(lead).model_dump(),
            "Lead retrieved successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving lead: {str(e)}"
        )


@router.put("/leads/{lead_id}", response_model=dict)
async def update_lead(
    lead_id: int,
    lead_data: LeadUpdate,
    db: AsyncSession = Depends(get_db),
    sync_crm: bool = False
):
    """Update a lead."""
    try:
        lead = await DatabaseService.get_lead(db, lead_id)
        if not lead:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Lead with ID {lead_id} not found"
            )
        
        updated_lead = await DatabaseService.update_lead(db, lead_id, lead_data)
        
        # Optionally sync to CRM
        if sync_crm and updated_lead:
            crm_id = await crm_service.sync_lead(updated_lead, provider="hubspot")
            if crm_id and not updated_lead.crm_id:
                await DatabaseService.update_lead(
                    db,
                    lead_id,
                    LeadUpdate(crm_id=crm_id)
                )
                updated_lead.crm_id = crm_id
        
        return build_response(
            LeadResponse.model_validate(updated_lead).model_dump(),
            "Lead updated successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating lead: {str(e)}"
        )


@router.delete("/leads/{lead_id}", response_model=dict)
async def delete_lead(
    lead_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete a lead."""
    try:
        success = await DatabaseService.delete_lead(db, lead_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Lead with ID {lead_id} not found"
            )
        
        return build_response(None, "Lead deleted successfully")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting lead: {str(e)}"
        )


@router.post("/leads/{lead_id}/sync-crm", response_model=dict)
async def sync_lead_to_crm(
    lead_id: int,
    provider: str = "hubspot",
    db: AsyncSession = Depends(get_db)
):
    """Manually sync a lead to CRM."""
    try:
        lead = await DatabaseService.get_lead(db, lead_id)
        if not lead:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Lead with ID {lead_id} not found"
            )
        
        crm_id = await crm_service.sync_lead(lead, provider=provider)
        if crm_id:
            await DatabaseService.update_lead(
                db,
                lead_id,
                LeadUpdate(crm_id=crm_id)
            )
            return build_response(
                {"crm_id": crm_id, "provider": provider},
                "Lead synced to CRM successfully"
            )
        else:
            return build_error_response("Failed to sync lead to CRM")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error syncing lead to CRM: {str(e)}"
        )

