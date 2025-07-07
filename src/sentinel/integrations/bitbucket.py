"""Bitbucket integration for fetching code and repository information"""

from typing import Dict, List, Optional

import httpx
from atlassian import Bitbucket

from sentinel.core.config import settings
from sentinel.core.logging import get_logger

logger = get_logger(__name__)


class BitbucketClient:
    """Client for interacting with Bitbucket API"""
    
    def __init__(self):
        self.client = Bitbucket(
            url=settings.BITBUCKET_API_URL,
            token=settings.BITBUCKET_ACCESS_TOKEN,
        )
    
    async def get_commit_diff(
        self,
        workspace: str,
        repo_slug: str,
        commit_id: str
    ) -> str:
        """Get the diff for a specific commit"""
        
        logger.info("Fetching commit diff", extra={
            "workspace": workspace,
            "repo": repo_slug,
            "commit": commit_id
        })
        
        try:
            # Use httpx for async requests
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.BITBUCKET_API_URL}/repositories/{workspace}/{repo_slug}/diff/{commit_id}",
                    headers={"Authorization": f"Bearer {settings.BITBUCKET_ACCESS_TOKEN}"}
                )
                response.raise_for_status()
                return response.text
        except Exception as e:
            logger.error("Failed to fetch commit diff", extra={"error": str(e)})
            raise
    
    async def get_file_content(
        self,
        workspace: str,
        repo_slug: str,
        file_path: str,
        ref: str = "main"
    ) -> str:
        """Get content of a file from repository"""
        
        logger.info("Fetching file content", extra={
            "workspace": workspace,
            "repo": repo_slug,
            "file": file_path,
            "ref": ref
        })
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.BITBUCKET_API_URL}/repositories/{workspace}/{repo_slug}/src/{ref}/{file_path}",
                    headers={"Authorization": f"Bearer {settings.BITBUCKET_ACCESS_TOKEN}"}
                )
                response.raise_for_status()
                return response.text
        except Exception as e:
            logger.error("Failed to fetch file content", extra={"error": str(e)})
            raise
    
    async def list_modified_files(
        self,
        workspace: str,
        repo_slug: str,
        commit_id: str
    ) -> List[Dict[str, str]]:
        """List files modified in a commit"""
        
        logger.info("Listing modified files", extra={
            "workspace": workspace,
            "repo": repo_slug,
            "commit": commit_id
        })
        
        # TODO: Implement using Bitbucket API
        return []