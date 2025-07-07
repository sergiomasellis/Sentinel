"""Test run database models"""

from enum import Enum
from typing import Optional

from sqlalchemy import JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from sentinel.models.base import BaseModel


class TestRunStatus(str, Enum):
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TestRun(BaseModel):
    """Test run model"""
    
    __tablename__ = "test_runs"
    
    # Repository information
    repository_url: Mapped[str] = mapped_column(String(512), nullable=False)
    branch: Mapped[str] = mapped_column(String(256), nullable=False)
    commit_id: Mapped[str] = mapped_column(String(64), nullable=False)
    
    # Optional Jira integration
    jira_ticket_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    
    # Test run status
    status: Mapped[TestRunStatus] = mapped_column(
        String(32),
        default=TestRunStatus.QUEUED,
        nullable=False
    )
    
    # Test configuration
    test_types: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    
    # Results
    total_tests: Mapped[int] = mapped_column(default=0, nullable=False)
    passed_tests: Mapped[int] = mapped_column(default=0, nullable=False)
    failed_tests: Mapped[int] = mapped_column(default=0, nullable=False)
    auto_healed_tests: Mapped[int] = mapped_column(default=0, nullable=False)
    
    # Detailed results and logs
    results: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)