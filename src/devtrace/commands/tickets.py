"""
DevTrace command: List all open Jira tickets assigned to the user.
"""

import typer
from rich.console import Console
from rich.table import Table
from datetime import datetime
from devtrace.utils.config import Config, ConfigError
from devtrace.utils.jira_client import JiraClient, JiraError

app = typer.Typer(name="tickets")
console = Console()


@app.command(name="list")
def list_tickets(
    status: str = typer.Option(
        "Open",
        "--status",
        "-s",
        help="Filter by ticket status (e.g., 'Open', 'In Progress', 'Done')"
    ),
    limit: int = typer.Option(
        None,
        "--limit",
        "-l",
        help="Limit number of tickets displayed"
    ),
):
    """
    Fetch and display all open Jira tickets assigned to you.

    Output: Clean tabulated console view with clickable links.
    """
    try:
        # Load config and initialize Jira client
        config = Config()
        jira = JiraClient(config)

        console.print("🔍 Fetching your Jira tickets...", style="cyan")
        tickets = jira.get_user_tickets(status_filter=status)

        if not tickets:
            console.print(
                f"✨ No tickets found with status '{status}'",
                style="yellow"
            )
            return

        # Apply limit if specified
        if limit:
            tickets = tickets[:limit]

        # Create rich table
        table = Table(title=f"📋 Your Jira Tickets (Status: {status})", show_header=True, header_style="bold cyan")
        table.add_column("Ticket ID", style="bright_blue", no_wrap=True)
        table.add_column("Summary", style="white")
        table.add_column("Status", style="green")
        table.add_column("Created", style="dim")
        table.add_column("Updated", style="dim")
        table.add_column("Due Date", style="yellow")
        table.add_column("Link", style="blue underline")

        for ticket in tickets:
            created_date = _format_date(ticket["created"])
            updated_date = _format_date(ticket["updated"])
            due_date = _format_date(ticket["duedate"]) if ticket["duedate"] else "—"

            # Truncate summary if too long
            summary = ticket["summary"]
            if len(summary) > 50:
                summary = summary[:47] + "..."

            table.add_row(
                ticket["key"],
                summary,
                ticket["status"],
                created_date,
                updated_date,
                due_date,
                ticket["url"],
            )

        console.print(table)
        console.print(f"\n✅ Showing {len(tickets)} ticket(s)")

    except ConfigError as e:
        console.print(f"❌ Configuration Error: {e}", style="red")
        raise typer.Exit(code=1)
    except JiraError as e:
        console.print(f"❌ Jira Error: {e}", style="red")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"❌ Unexpected Error: {e}", style="red")
        raise typer.Exit(code=1)


@app.callback(invoke_without_command=True)
def tickets_command(ctx: typer.Context):
    """
    Main tickets command - alias for 'devtrace tickets list'.
    """
    if ctx.invoked_subcommand is None:
        # Default to list if no subcommand provided
        ctx.invoke(list_tickets)


def _format_date(date_str: str) -> str:
    """Format date string to readable format."""
    if not date_str:
        return "—"
    try:
        # Parse ISO format date
        date_obj = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return date_obj.strftime("%Y-%m-%d")
    except Exception:
        return date_str[:10] if len(date_str) >= 10 else date_str
