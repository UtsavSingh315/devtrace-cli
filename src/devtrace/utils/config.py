"""
Configuration parser for DevTrace local TOML configuration.
Handles secure reading of Jira and Git credentials.
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
import toml
from rich.console import Console

console = Console()


class ConfigError(Exception):
    """Raised when configuration is invalid or missing."""
    pass


class Config:
    """Manages DevTrace configuration from TOML files."""

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize Config with optional custom path.

        Args:
            config_path: Optional path to config file. Defaults to ~/.devtrace/configs/local/local_config.toml
        """
        if config_path is None:
            # Use OS-aware path resolution
            if os.name == "nt":  # Windows
                base_path = Path(os.getenv("USERPROFILE", "~")).expanduser()
            else:  # Unix-like
                base_path = Path.home()

            config_path = base_path / ".devtrace" / "configs" / "local" / "local_config.toml"

        self.config_path = Path(config_path).expanduser()
        self._data: Dict[str, Any] = {}

        if not self.config_path.exists():
            raise ConfigError(
                f"Configuration file not found at {self.config_path}\n"
                "Please run 'devtrace init' to set up your configuration."
            )

        self._load_config()

    def _load_config(self) -> None:
        """Load and parse the TOML configuration file."""
        try:
            with open(self.config_path, "r") as f:
                self._data = toml.load(f)
        except toml.TomlDecodeError as e:
            raise ConfigError(f"Invalid TOML syntax in {self.config_path}: {e}")
        except IOError as e:
            raise ConfigError(f"Failed to read configuration: {e}")

    def get_jira_config(self) -> Dict[str, str]:
        """
        Get Jira API configuration.

        Returns:
            Dictionary with 'host', 'email', and 'api_token' keys.

        Raises:
            ConfigError: If Jira config is missing or incomplete.
        """
        jira_config = self._data.get("jira", {})

        required_keys = ["host", "email", "api_token"]
        missing_keys = [key for key in required_keys if key not in jira_config]

        if missing_keys:
            raise ConfigError(
                f"Missing Jira configuration keys: {', '.join(missing_keys)}\n"
                "Please add these to your ~/.devtrace/configs/local/local_config.toml"
            )

        return {
            "host": jira_config["host"],
            "email": jira_config["email"],
            "api_token": jira_config["api_token"],
        }

    def get_git_config(self) -> Dict[str, str]:
        """
        Get Git API configuration.

        Returns:
            Dictionary with 'github_token' and optional 'github_user' keys.

        Raises:
            ConfigError: If Git config is missing.
        """
        git_config = self._data.get("git", {})

        if "github_token" not in git_config:
            raise ConfigError(
                "Missing Git configuration: 'github_token'\n"
                "Please add this to your ~/.devtrace/configs/local/local_config.toml"
            )

        return {
            "github_token": git_config["github_token"],
            "github_user": git_config.get("github_user", ""),
        }

    def get_active_context(self) -> Dict[str, Any]:
        """
        Get the current active ticket context.

        Returns:
            Dictionary with 'ticket_id', 'started_at', and 'branch' keys.
        """
        active = self._data.get("active", {})
        return {
            "ticket_id": active.get("ticket_id"),
            "started_at": active.get("started_at"),
            "branch": active.get("branch"),
        }

    def set_active_context(self, ticket_id: str, branch: str = "main") -> None:
        """
        Update the active ticket context.

        Args:
            ticket_id: The active Jira ticket ID.
            branch: The active Git branch.
        """
        from datetime import datetime, timezone

        self._data["active"] = {
            "ticket_id": ticket_id,
            "started_at": datetime.now(timezone.utc).isoformat(),
            "branch": branch,
        }
        self._save_config()

    def _save_config(self) -> None:
        """Save current configuration back to TOML file."""
        try:
            with open(self.config_path, "w") as f:
                toml.dump(self._data, f)
        except IOError as e:
            raise ConfigError(f"Failed to save configuration: {e}")

    def get_all(self) -> Dict[str, Any]:
        """Return the entire configuration dictionary."""
        return self._data
