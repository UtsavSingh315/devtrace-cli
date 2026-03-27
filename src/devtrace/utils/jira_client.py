"""
Jira API client wrapper for DevTrace.
Handles authentication and common Jira operations.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from devtrace.utils.config import Config, ConfigError
from rich.console import Console

console = Console()


class JiraError(Exception):
    """Raised when Jira API operations fail."""
    pass


class JiraClient:
    """Client for interacting with Jira API."""

    def __init__(self, config: Optional[Config] = None):
        """
        Initialize Jira client with credentials from config.

        Args:
            config: Config object. If None, loads from default location.

        Raises:
            ConfigError: If Jira credentials are missing.
            JiraError: If authentication fails.
        """
        if config is None:
            config = Config()

        self.config = config
        jira_config = config.get_jira_config()

        self.host = jira_config["host"]
        self.email = jira_config["email"]
        self.api_token = jira_config["api_token"]

        # Lazy import to avoid dependency errors during development
        try:
            from jira import JIRA
            self.jira = JIRA(
                server=self.host,
                basic_auth=(self.email, self.api_token),
                options={"agile_rest_path": "agile"}
            )
        except ImportError:
            raise JiraError(
                "Jira client library not installed. "
                "Install it with: pip install jira"
            )
        except Exception as e:
            raise JiraError(f"Failed to authenticate with Jira: {e}")

    def get_user_tickets(self, status_filter: str = "Open") -> List[Dict[str, Any]]:
        """
        Fetch all open Jira tickets assigned to the authenticated user.

        Args:
            status_filter: JQL status filter. Default is "Open".

        Returns:
            List of ticket dictionaries with relevant fields.

        Raises:
            JiraError: If the API call fails.
        """
        try:
            # JQL query for tickets assigned to current user
            jql = f'assignee = currentUser() AND status = "{status_filter}"'
            issues = self.jira.search_issues(
                jql,
                maxResults=100,
                fields=[
                    "key",
                    "summary",
                    "status",
                    "created",
                    "updated",
                    "duedate",
                    "description",
                    "assignee",
                    "reporter",
                    "priority",
                    "comment",
                ]
            )

            tickets = []
            for issue in issues:
                tickets.append(self._format_ticket(issue))

            return tickets
        except Exception as e:
            raise JiraError(f"Failed to fetch user tickets: {e}")

    def get_ticket_details(self, ticket_id: str) -> Dict[str, Any]:
        """
        Fetch full details of a specific Jira ticket.

        Args:
            ticket_id: The ticket key (e.g., "PROJ-123").

        Returns:
            Dictionary with full ticket details.

        Raises:
            JiraError: If the ticket is not found or API call fails.
        """
        try:
            issue = self.jira.issue(
                ticket_id,
                fields=[
                    "key",
                    "summary",
                    "description",
                    "status",
                    "assignee",
                    "reporter",
                    "priority",
                    "created",
                    "updated",
                    "duedate",
                    "comment",
                    "changelog",
                ]
            )
            return self._format_ticket_details(issue)
        except Exception as e:
            raise JiraError(f"Failed to fetch ticket {ticket_id}: {e}")

    def post_comment(self, ticket_id: str, comment: str) -> Dict[str, str]:
        """
        Post a comment to a Jira ticket.

        Args:
            ticket_id: The ticket key (e.g., "PROJ-123").
            comment: The comment text.

        Returns:
            Dictionary with 'id' and 'self' (URL) of the posted comment.

        Raises:
            JiraError: If the API call fails.
        """
        try:
            comment_obj = self.jira.add_comment(ticket_id, comment)
            return {
                "id": comment_obj.id,
                "self": comment_obj.self,
            }
        except Exception as e:
            raise JiraError(f"Failed to post comment to {ticket_id}: {e}")

    def _format_ticket(self, issue: Any) -> Dict[str, Any]:
        """Format a Jira issue object into a dictionary."""
        return {
            "key": issue.key,
            "summary": issue.fields.summary,
            "status": issue.fields.status.name if issue.fields.status else "Unknown",
            "created": issue.fields.created,
            "updated": issue.fields.updated,
            "duedate": issue.fields.duedate,
            "url": f"{self.host}/browse/{issue.key}",
        }

    def _format_ticket_details(self, issue: Any) -> Dict[str, Any]:
        """Format a Jira issue object with full details."""
        comments = []
        if issue.fields.comment and issue.fields.comment.comments:
            # Get last 5 comments
            for comment in issue.fields.comment.comments[-5:]:
                comments.append({
                    "author": comment.author.displayName if comment.author else "Unknown",
                    "body": comment.body,
                    "created": comment.created,
                })

        return {
            "key": issue.key,
            "summary": issue.fields.summary,
            "description": issue.fields.description or "No description",
            "status": issue.fields.status.name if issue.fields.status else "Unknown",
            "assignee": issue.fields.assignee.displayName if issue.fields.assignee else "Unassigned",
            "reporter": issue.fields.reporter.displayName if issue.fields.reporter else "Unknown",
            "priority": issue.fields.priority.name if issue.fields.priority else "Unknown",
            "created": issue.fields.created,
            "updated": issue.fields.updated,
            "duedate": issue.fields.duedate,
            "comments": comments,
            "url": f"{self.host}/browse/{issue.key}",
        }
