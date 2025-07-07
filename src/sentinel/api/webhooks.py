"""Webhook endpoints for CI/CD integration"""

from typing import Dict

from fastapi import APIRouter, BackgroundTasks, HTTPException, Header, Request, status
from pydantic import BaseModel

from sentinel.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


class WebhookPayload(BaseModel):
    """Generic webhook payload"""
    event_type: str
    repository: Dict
    branch: str
    commit: str
    metadata: Dict = {}


@router.post("/webhooks/bitbucket", status_code=status.HTTP_202_ACCEPTED)
async def bitbucket_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_event_key: str = Header(None)
) -> Dict[str, str]:
    """Handle Bitbucket webhooks"""
    
    logger.info("Received Bitbucket webhook", extra={"event_key": x_event_key})
    
    # TODO: Validate webhook signature
    # TODO: Parse webhook payload based on event type
    # TODO: Queue test run if appropriate
    
    return {"status": "accepted", "message": "Webhook processed"}


@router.post("/webhooks/harness", status_code=status.HTTP_202_ACCEPTED)
async def harness_webhook(
    payload: WebhookPayload,
    background_tasks: BackgroundTasks
) -> Dict[str, str]:
    """Handle Harness CI webhooks"""
    
    logger.info("Received Harness webhook", extra={
        "event_type": payload.event_type,
        "repository": payload.repository.get("name"),
        "branch": payload.branch,
        "commit": payload.commit,
    })
    
    # TODO: Process webhook and create test run
    
    return {"status": "accepted", "message": "Webhook processed"}