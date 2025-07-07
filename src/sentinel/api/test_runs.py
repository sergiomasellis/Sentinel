"""Test run management endpoints"""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from sentinel.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


class TestRunRequest(BaseModel):
    """Request model for creating a test run"""
    repository_url: str
    branch: str
    commit_id: str
    jira_ticket_id: Optional[str] = None
    test_types: List[str] = Field(default=["e2e", "integration"])


class TestRunResponse(BaseModel):
    """Response model for test run"""
    run_id: UUID
    status: str
    message: str


@router.post("/test-runs", response_model=TestRunResponse, status_code=status.HTTP_201_CREATED)
async def create_test_run(request: TestRunRequest) -> TestRunResponse:
    """Create a new test run"""
    logger.info("Creating test run", extra={
        "repository": request.repository_url,
        "branch": request.branch,
        "commit": request.commit_id,
        "jira_ticket": request.jira_ticket_id,
    })
    
    # TODO: Implement actual test run creation logic
    # This will involve:
    # 1. Validating the request
    # 2. Creating a test run record
    # 3. Queuing the test generation task
    # 4. Returning the run ID
    
    from uuid import uuid4
    run_id = uuid4()
    
    return TestRunResponse(
        run_id=run_id,
        status="queued",
        message="Test run has been queued for processing"
    )


@router.get("/test-runs/{run_id}", response_model=TestRunResponse)
async def get_test_run(run_id: UUID) -> TestRunResponse:
    """Get status of a test run"""
    logger.info("Getting test run status", extra={"run_id": str(run_id)})
    
    # TODO: Implement actual test run retrieval
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Test run {run_id} not found"
    )