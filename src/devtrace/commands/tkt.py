"""
DevTrace command: View full details of a specific Jira ticket.
"""

import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax
from datetime import datetime
from devtrace.utils.config import Config, ConfigError
from devtrace.utils.jira_client import JiraClient, JiraError

console = Console()


def ticket_details(
    ticket_id: str = typer.Argument(..., help="Ticket ID (e.g., PROJ-123)"),
    show_comments: bool = typer.Option(
        True,
        "--comments/--no-comments",
        help="Show recent comments"
    ),
):
    """
    Fetch and display full details of a specific Jira ticket.

    Example:
        devtrace tkt PROJ-123
        devtrace tkt DT-21 --no-comments
    """
    try:
        # Load config and initialize Jira client
        config = Config()
        jira = JiraClient(config)

        console.print(f"🔍 Fetching ticket {ticket_id}...", style="cyan")
        ticket = jira.get_ticket_details(ticket_id)

        # Title panel
        title = f"{ticket['key']} — {ticket['summary']}"
        console.print(Panel(title, style="bold bright_blue"))

        # Status and metadata
        metadata_lines = [
            f"[bold cyan]Status:[/bold cyan] [green]{ticket['status']}[/green]",
            f"[bold cyan]Priority:[/bold cyan] {_format_priority(ticket['priority'])}",
            f"[bold cyan]Assignee:[/bold cyan] {ticket['assignee']}",
            f"[bold cyan]Reporter:[/bold cyan] {ticket['reporter']}",
            f"[bold cyan]Created:[/bold cyan] {_format_datetime(ticket['created'])}",
            f"[bold cyan]Updated:[/bold cyan] {_format_datetime(ticket['updated'])}",
        ]

        if ticket["duedate"]:
            metadata_lines.append(
                f"[bold cyan]Due Date:[/bold cyan] [yellow]{ticket['duedate']}[/yellow]"
            )

        console.print("\n".join(metadata_lines))

        # Description
        console.print("\n[bold cyan]📝 Description:[/bold cyan]")
        console.print(ticket["description"])

        # Comments
        if show_comments and ticket["comments"]:
            console.print("\n[bold cyan]💬 Recent Comments:[/bold cyan]")
            for i, comment in enumerate(ticket["comments"], 1):
                author = comment["author"]
                body = comment["body"]
                created = _format_datetime(comment["created"])

                comment_text = (
                    f"\n[dim][{i}][/dim] [bold]{author}[/bold] "
                    f"[dim]({created})[/dim]\n{body}"
                )
                console.print(comment_text)

        # Footer with link
        console.print(f"\n🔗 [link={ticket['url']}]Open in Jira[/link]", style="dim blue")

    except ConfigError as e:
        console.print(f"❌ Configuration Error: {e}", style="red")
        raise typer.Exit(code=1)
    except JiraError as e:
        console.print(f"❌ Jira Error: {e}", style="red")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"❌ Unexpected Error: {e}", style="red")
        raise typer.Exit(code=1)


def _format_priority(priority: str) -> str:
    """Format priority with color coding."""
    colors = {
        "Highest": "red",
        "High": "yellow",
        "Medium": "cyan",
        "Low": "green",
        "Lowest": "dim green",
    }
    color = colors.get(priority, "white")
    return f"[{color}]{priority}[/{color}]"


def _format_datetime(date_str: str) -> str:
    """Format ISO datetime string to readable format."""
    if not date_str:
        return "—"
    try:
        date_obj = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return date_obj.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return date_str
