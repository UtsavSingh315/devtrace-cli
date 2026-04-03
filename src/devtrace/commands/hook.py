"""
Git hook integration for automated Jira ticket updates.
Posts commit details to the active Jira ticket automatically.
"""

import typer
from pathlib import Path
from rich.console import Console
from typing import Optional, List, Tuple
from devtrace.utils.config import Config, ConfigError
from devtrace.utils.jira_client import JiraClient, JiraError
import subprocess
import re

app = typer.Typer(name="hook")
console = Console()


class GitError(Exception):
    """Raised when Git operations fail."""
    pass


def get_current_commit_info() -> dict:
    """
    Get details of the current/latest commit.

    Returns:
        Dictionary with 'hash', 'message', 'files' keys.
    """
    try:
        # Get commit hash
        commit_hash = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            text=True
        ).strip()

        # Get commit message
        commit_message = subprocess.check_output(
            ["git", "log", "-1", "--pretty=%B"],
            text=True
        ).strip()

        # Get files changed in this commit
        files_changed = subprocess.check_output(
            ["git", "show", "--name-status", "--pretty=", commit_hash],
            text=True
        ).strip().split("\n")

        # Get diff stats
        diff_stats = subprocess.check_output(
            ["git", "show", "--stat", "--oneline", commit_hash],
            text=True
        ).strip().split("\n")[-1]  # Last line has the summary

        return {
            "hash": commit_hash[:7],  # Short hash
            "message": commit_message,
            "files": [f for f in files_changed if f],
            "stats": diff_stats,
        }
    except subprocess.CalledProcessError as e:
        raise GitError(f"Failed to get commit info: {e}")


def get_files_diff_stats(commit_hash: str) -> List[Tuple[str, int, int]]:
    """
    Get detailed diff stats (additions/deletions) per file.

    Returns:
        List of tuples: (filename, additions, deletions)
    """
    try:
        diff_output = subprocess.check_output(
            ["git", "diff", f"{commit_hash}^..{commit_hash}", "--numstat"],
            text=True
        ).strip().split("\n")

        stats = []
        for line in diff_output:
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) >= 3:
                additions = int(parts[0]) if parts[0] != "-" else 0
                deletions = int(parts[1]) if parts[1] != "-" else 0
                filename = parts[2]
                stats.append((filename, additions, deletions))

        return stats
    except (subprocess.CalledProcessError, ValueError) as e:
        console.print(f"[yellow]Warning: Could not get detailed diff stats: {e}[/yellow]")
        return []


@app.command(name="post-commit")
def post_commit_hook(
    skip_if_wip: bool = typer.Option(
        True,
        "--skip-wip/--no-skip-wip",
        help="Skip posting if commit message contains [WIP]"
    ),
):
    """
    Post-commit Git hook: Automatically posts commit details to active Jira ticket.

    This hook is triggered after a successful commit.
    It fetches the commit details and posts them to the currently active ticket.

    Usage (in .devtrace/hooks/post-commit):
        #!/bin/sh
        devtrace hook post-commit
        exit $?
    """
    try:
        config = Config()
        
        # Get commit info
        commit_info = get_current_commit_info()
        
        # Extract ticket ID from commit message (format: TICKET-ID | TYPE : message)
        ticket_match = re.match(r'^([A-Z]+-\d+)', commit_info["message"])
        
        if not ticket_match:
            # Fallback to active context
            active_context = config.get_active_context()
            ticket_id = active_context.get("ticket_id")
            
            if not ticket_id:
                console.print("[yellow]⚠️  No ticket ID in commit message or active context. Skipping auto-comment.[/yellow]")
                raise typer.Exit(code=0)
        else:
            ticket_id = ticket_match.group(1)

        # Skip if WIP
        if skip_if_wip and "[WIP]" in commit_info["message"]:
            console.print("[yellow]⏭️  Skipping WIP commit (contains [WIP] in message)[/yellow]")
            raise typer.Exit(code=0)

        # Build comment payload
        files_diff = get_files_diff_stats(commit_info["hash"])

        files_section = ""
        if files_diff:
            files_section = "\n**Files Changed:**\n"
            for filename, adds, deletes in files_diff:
                files_section += f"- {filename} (+{adds}, -{deletes})\n"
        else:
            # Fallback to simple file list
            files_section = "\n**Files Changed:**\n"
            for file in commit_info["files"]:
                if file:
                    files_section += f"- {file}\n"

        comment_payload = (
            f"🤖 **Automated DevTrace Update: Code committed**\n\n"
            f"**Commit Message:**\n```\n{commit_info['message']}\n```\n\n"
            f"**Commit Hash:** `{commit_info['hash']}`\n"
            f"{files_section}"
        )

        # Post comment to Jira
        jira = JiraClient(config)
        result = jira.post_comment(ticket_id, comment_payload)

        console.print(
            f"✅ Auto-comment posted to {ticket_id}",
            style="green"
        )
        console.print(f"[dim]Comment ID: {result['id']}[/dim]")

    except ConfigError as e:
        console.print(f"[yellow]⚠️  Config Error: {e}[/yellow]")
        raise typer.Exit(code=0)
    except JiraError as e:
        console.print(f"[yellow]⚠️  Jira Error: {e}. Commit succeeded; skipping auto-comment.[/yellow]")
        raise typer.Exit(code=0)
    except GitError as e:
        console.print(f"[red]❌ Git Error: {e}[/red]")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[yellow]⚠️  Unexpected error: {e}. Commit succeeded; skipping auto-comment.[/yellow]")
        raise typer.Exit(code=0)


@app.command(name="prepare-commit-msg")
def prepare_commit_msg_hook(
    commit_msg_filepath: str = typer.Argument(None, help="Path to commit message file"),
    commit_source: str = typer.Argument("message", help="Commit source type"),
):
    """
    Prepare-commit-msg Git hook: Pre-fill commit message with active ticket ID.

    This hook is triggered before the commit message editor opens.
    It prepends the active ticket ID to the commit message if not already present.

    Usage (in .devtrace/hooks/prepare-commit-msg):
        #!/bin/sh
        devtrace hook prepare-commit-msg "$1" "$2"
        exit $?
    """
    if not commit_msg_filepath:
        raise typer.Exit(code=0)

    try:
        config = Config()
        active_context = config.get_active_context()
        ticket_id = active_context.get("ticket_id")

        if not ticket_id:
            raise typer.Exit(code=0)

        # Read current commit message
        msg_file = Path(commit_msg_filepath)
        current_msg = msg_file.read_text().strip()

        # Only auto-prepend for new commit messages (not merges, squashes, etc.)
        if commit_source not in ["message", ""]:
            raise typer.Exit(code=0)

        # Don't modify if ticket ID already present
        if ticket_id in current_msg:
            raise typer.Exit(code=0)

        # Prepend ticket ID
        updated_msg = f"{ticket_id} | {current_msg}"
        msg_file.write_text(updated_msg)

        console.print(f"[dim]📍 Prepended {ticket_id} to commit message[/dim]")

    except ConfigError:
        pass  # Silently skip if config is missing
    except Exception as e:
        console.print(f"[dim]Warning: {e}[/dim]")

    raise typer.Exit(code=0)


@app.callback(invoke_without_command=True)
def hook_command(ctx: typer.Context):
    """
    Git hook management for DevTrace.

    Automates Jira ticket updates on commits.
    """
    if ctx.invoked_subcommand is None:
        console.print("Use 'devtrace hook --help' for available subcommands", style="yellow")
