"""
DevTrace command: Post a comment to the active or specified Jira ticket.
"""

import typer
from rich.console import Console
from devtrace.utils.config import Config, ConfigError
from devtrace.utils.jira_client import JiraClient, JiraError

app = typer.Typer(name="comment")
console = Console()


@app.command()
def post_comment(
    message: str = typer.Argument(..., help="Comment message"),
    ticket_id: str = typer.Option(
        None,
        "--ticket",
        "-t",
        help="Target ticket ID (uses active context if not specified)"
    ),
):
    """
    Post a comment to a Jira ticket.

    If no ticket ID is provided, uses the currently active ticket from context.

    Examples:
        devtrace comment "Great progress on this task!"
        devtrace comment "Fixed the bug" --ticket DT-25
        devtrace comment "Updated tests" -t PROJ-456
    """
    try:
        config = Config()

        # Determine target ticket
        if ticket_id is None:
            active_context = config.get_active_context()
            ticket_id = active_context.get("ticket_id")

            if not ticket_id:
                console.print(
                    "❌ No active ticket in context. Specify with --ticket",
                    style="red"
                )
                raise typer.Exit(code=1)
            else:
                console.print(
                    f"📍 Using active ticket: {ticket_id}",
                    style="yellow"
                )

        # Initialize Jira client and post comment
        jira = JiraClient(config)
        console.print(f"📝 Posting comment to {ticket_id}...", style="cyan")

        result = jira.post_comment(ticket_id, message)

        console.print(
            f"✅ Comment posted successfully!",
            style="green"
        )
        console.print(f"📌 Comment ID: {result['id']}")
        console.print(f"🔗 [link={result['self']}]View in Jira[/link]", style="dim blue")

    except ConfigError as e:
        console.print(f"❌ Configuration Error: {e}", style="red")
        raise typer.Exit(code=1)
    except JiraError as e:
        console.print(f"❌ Jira Error: {e}", style="red")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"❌ Unexpected Error: {e}", style="red")
        raise typer.Exit(code=1)
