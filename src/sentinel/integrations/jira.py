"""Jira integration for fetching user stories and requirements"""

from typing import Dict, Optional

from atlassian import Jira

from sentinel.core.config import settings
from sentinel.core.logging import get_logger

logger = get_logger(__name__)


class JiraClient:
    """Client for interacting with Jira API"""
    
    def __init__(self):
        self.client = Jira(
            url=settings.JIRA_URL,
            username=settings.JIRA_EMAIL,
            password=settings.JIRA_API_TOKEN,
        )
    
    async def get_issue_details(self, issue_key: str) -> Optional[Dict]:
        """Get details of a Jira issue including user story and acceptance criteria"""
        
        logger.info("Fetching Jira issue", extra={"issue_key": issue_key})
        
        try:
            issue = self.client.issue(issue_key)
            
            # Extract relevant fields
            details = {
                "key": issue_key,
                "summary": issue["fields"]["summary"],
                "description": issue["fields"]["description"],
                "issue_type": issue["fields"]["issuetype"]["name"],
                "status": issue["fields"]["status"]["name"],
                "acceptance_criteria": self._extract_acceptance_criteria(issue),
            }
            
            return details
        except Exception as e:
            logger.error("Failed to fetch Jira issue", extra={
                "issue_key": issue_key,
                "error": str(e)
            })
            return None
    
    def _extract_acceptance_criteria(self, issue: Dict) -> str:
        """Extract acceptance criteria from issue fields"""
        
        # This depends on how acceptance criteria are stored in your Jira
        # Could be in description, custom field, or comments
        
        # Check custom fields
        for field_name, field_value in issue["fields"].items():
            if "acceptance" in field_name.lower() and field_value:
                return str(field_value)
        
        # Fallback to parsing from description
        description = issue["fields"].get("description", "")
        if "acceptance criteria" in description.lower():
            # Simple extraction - might need more sophisticated parsing
            parts = description.lower().split("acceptance criteria")
            if len(parts) > 1:
                return parts[1].strip()
        
        return ""
    
    async def add_comment(self, issue_key: str, comment: str) -> bool:
        """Add a comment to a Jira issue"""
        
        logger.info("Adding comment to Jira issue", extra={"issue_key": issue_key})
        
        try:
            self.client.issue_add_comment(issue_key, comment)
            return True
        except Exception as e:
            logger.error("Failed to add comment", extra={
                "issue_key": issue_key,
                "error": str(e)
            })
            return False