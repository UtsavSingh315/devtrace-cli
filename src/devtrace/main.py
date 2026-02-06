import typer
from rich.console import Console
from devtrace.commands import hello, version
from devtrace.commands.init import app as init_app
from devtrace.commands.validate import app as validate_app

app = typer.Typer(name="devtrace", add_completion=False)
console = Console()


app.command()(hello.hello)
app.command()(version.version)
app.add_typer(init_app, name="init")
app.add_typer(validate_app, name="validate")

if __name__ == "__main__":
    app()