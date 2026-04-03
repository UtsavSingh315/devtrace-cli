import typer
from rich.console import Console

# Define version here for PyInstaller compatibility
__version__ = "0.1.0"

console = Console()

def version():
    """Show version"""
    console.print(f"devtrace version {__version__}")