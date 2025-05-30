from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from ..services.n8n_service import N8NService

router = APIRouter()

class WorkflowRequest(BaseModel):
    workflow_id: str
    data: Dict[str, Any]

class WorkflowResponse(BaseModel):
    execution_id: str
    status: str
    result: Optional[Dict[str, Any]] = None

@router.post("/trigger", response_model=WorkflowResponse)
async def trigger_workflow(request: WorkflowRequest):
    try:
        n8n_service = N8NService()
        result = await n8n_service.trigger_workflow(
            request.workflow_id,
            request.data
        )
        
        return WorkflowResponse(
            execution_id=result.get("id"),
            status=result.get("status", "running"),
            result=result.get("data")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{execution_id}", response_model=WorkflowResponse)
async def get_workflow_status(execution_id: str):
    try:
        n8n_service = N8NService()
        result = await n8n_service.get_workflow_status(execution_id)
        
        return WorkflowResponse(
            execution_id=execution_id,
            status=result.get("status", "unknown"),
            result=result.get("data")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/workflow/{workflow_id}")
async def get_workflow_data(workflow_id: str):
    try:
        n8n_service = N8NService()
        return await n8n_service.get_workflow_data(workflow_id)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 