import typer
import toml
import subprocess
from rich.console import Console
from pathlib import Path

app = typer.Typer(
    invoke_without_command=True,
    help="Initialize devtrace project or specific components"
)
console = Console()

@app.callback()
def main_callback(
    ctx: typer.Context,
    # project_dir: str = typer.Argument(".devtrace", help="Path to initialize (default: current dir)"),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing files/folders")
):
    """Main initialization: Create project structure with folders and configs"""
    if ctx.invoked_subcommand is not None:
        return
    
    base_path = Path(".devtrace").resolve()
    
    if base_path.exists() and not force:
        console.print("[yellow]Directory already exists. Use --force to overwrite.[/]")
        raise typer.Exit(code=1)
    
    console.print(f"[bold green]Initializing main project in {base_path}[/]")
    
    # Folders
    folders = [
        base_path / "configs",
        base_path / "logs",
        base_path / "hooks"
    ]

    for folder in folders:
        try:
            folder.mkdir(parents=True, exist_ok=True)
            console.print(f"[dim]Created: {folder.relative_to(base_path)}[/]")
        except Exception as e:
            console.print(f"[red]Error creating {folder}: {e}[/]")
            raise typer.Exit(code=1)
    
    # Subfolders
    subfolders = [
        base_path / "configs" / "jira",
        base_path / "configs" / "git"
    ]
    for sub in subfolders:
        sub.mkdir(exist_ok=True)
        console.print(f"[dim]Created sub: {sub.relative_to(base_path)}[/]")
    
    # Configs 
    configs = {
        base_path / "configs" / "rules.toml": {
            "commit": {"pattern": "^[A-Z]+-\\d+\\s\\|\\s[A-Z]+\\s:\\s.+$", "strict": True},
            "ticket": {"pattern": "^[A-Z]+-\\d+$", "uppercase": True},
            "types": {"allowed": ["FEAT", "FIX", "INIT", "DOCS", "REFACTOR", "TEST", "CHORE"]},
            "severity": {"invalid_format": "error", "unknown_type": "error", "missing_ticket": "error"}
        },
    }
    for file_path, content in configs.items():
        if file_path.exists() and not force:
            console.print(f"[yellow]Skipping existing: {file_path.relative_to(base_path)}[/]")
            continue
        try:
            with file_path.open("w", encoding="utf-8") as f:
                toml.dump(content, f)
            console.print(f"[dim]Created config: {file_path.relative_to(base_path)}[/]")
        except Exception as e:
            console.print(f"[red]Error writing {file_path}: {e}[/]")
            raise typer.Exit(code=1)
    
    # Hook example
    hook_path = base_path / "hooks" / "commit-msg"
    hook_content = """#!/bin/sh
# devtrace commit-msg hook: Calls standalone devtrace executable

REPO_ROOT="$(git rev-parse --show-toplevel)"
RULES_FILE="$REPO_ROOT/.devtrace/configs/rules.toml"


devtrace validate commit "$1" --rules-path "$RULES_FILE" 

if [ $? -ne 0 ]; then
    exit 1
fi
"""
    hook_path.write_text(hook_content)
    hook_path.chmod(0o755)
    
    hooks_dir_rel = ".devtrace/hooks"
    try:
        # Check if it's a git repo
        subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], cwd=base_path.parent, check=True, capture_output=True)
        
        # Set the config (local to this repo)
        subprocess.run(["git", "config", "core.hooksPath", hooks_dir_rel], cwd=base_path.parent, check=True)
        console.print(f"[bold green]Set git core.hooksPath to {hooks_dir_rel}[/]")
        console.print("[dim]All hooks in .devtrace/hooks are now active![/]")
    except subprocess.CalledProcessError:
        console.print("[yellow]Not a git repo (run 'git init' first). Hooks generated but not activated.[/]")
    except FileNotFoundError:
        console.print("[red]Git not found in PATH. Manually set 'git config core.hooksPath .devtrace/hooks' after init.[/]")


    
    console.print("[bold green]Main initialization complete![/]")
    console.print("[dim]Run 'devtrace init --help' for component-specific init options.[/]")




# subcommands
@app.command()
def hooks():
    """Use to apply devtrace hooks as default git hooks"""
    base_path = Path(".devtrace").resolve()
    hooks_dir_rel = ".devtrace/hooks"
    try:
        # Check if it's a git repo
        subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], cwd=base_path.parent, check=True, capture_output=True)
        
        # Set the config (local to this repo)
        subprocess.run(["git", "config", "core.hooksPath", hooks_dir_rel], cwd=base_path.parent, check=True)
        console.print(f"[bold green]Set git core.hooksPath to {hooks_dir_rel}[/]")
        console.print("[dim]All hooks in .devtrace/hooks are now active![/]")
    except subprocess.CalledProcessError:
        console.print("[yellow]Not a git repo (run 'git init' first). Hooks generated but not activated.[/]")
    except FileNotFoundError:
        console.print("[red]Git not found in PATH. Manually set 'git config core.hooksPath .devtrace/hooks' after init.[/]")

@app.command()
def jira(
    config_path: str = typer.Option("configs/jira.toml", help="Path to Jira config file")
):
    """Initialize or update Jira-specific configs"""
    console.print(f"[yellow]Setting up Jira at {config_path}[/]")


@app.command()
def git(
    hook_dir: str = typer.Option("hooks", help="Directory for Git hooks")
):
    """Initialize Git hooks and configs"""
    console.print(f"[yellow]Setting up Git in {hook_dir}[/]")