"""Test run management endpoints"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from sentinel.core.config import settings
from sentinel.core.logging import get_logger
from sentinel.models.test_run import TestRun

# Database setup (TODO: Move to proper dependency injection)
engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncSession:
    """Database session dependency"""
    async with async_session() as session:
        yield session



router = APIRouter()
logger = get_logger(__name__)


class TestRunRequest(BaseModel):
    """Request model for creating a test run"""

    repository_url: str
    branch: str
    commit_id: str
    jira_ticket_id: str | None = None
    test_types: list[str] = Field(default=["e2e", "integration"])


class TestRunResponse(BaseModel):
    """Response model for test run"""

    run_id: UUID
    status: str
    message: str


class TestRunListResponse(BaseModel):
    """Response model for list of test runs"""

    test_runs: list[TestRunResponse]


@router.post(
    "/test-runs", response_model=TestRunResponse, status_code=status.HTTP_201_CREATED
)
async def create_test_run(request: TestRunRequest) -> TestRunResponse:
    """Create a new test run"""
    logger.info(
        "Creating test run",
        extra={
            "repository": request.repository_url,
            "branch": request.branch,
            "commit": request.commit_id,
            "jira_ticket": request.jira_ticket_id,
        },
    )

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
        message="Test run has been queued for processing",
    )


@router.get("/test-runs/{run_id}", response_model=TestRunResponse)
async def get_test_run(run_id: UUID) -> TestRunResponse:
    """Get status of a test run"""
    logger.info("Getting test run status", extra={"run_id": str(run_id)})

    # TODO: Implement actual test run retrieval

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Test run {run_id} not found"
    )


@router.get("/test-runs", response_model=TestRunListResponse)
async def get_all_test_runs(db: AsyncSession = Depends(get_db)) -> TestRunListResponse:
    """Get all test runs"""
    logger.info("Getting all test runs")

    try:
        # Query all test runs from database
        result = await db.execute(select(TestRun))
        test_runs = result.scalars().all()

        # Convert to response format
        test_run_responses = [
            TestRunResponse(
                run_id=test_run.id,
                status=test_run.status.value,
                message=f"Test run for {test_run.repository_url} on branch {test_run.branch}",
            )
            for test_run in test_runs
        ]

        return TestRunListResponse(test_runs=test_run_responses)

    except Exception as e:
        logger.error("Error retrieving test runs", extra={"error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve test runs",
        ) from e
