# commnad line tool using typer
from typing import Optional
import typer

# from __inti__.py import __version__ and __app_name__
from . import __version__, __app_name__

# create command line interface using typer
app = typer.Typer()


# function for version callbvack and call back decorator
def _version_callback(value: bool):
    if value:
        typer.echo(f"{__app_name__} version {__version__}")
        raise typer.Exit()

# define main() as a Typer callback using the @app.callback() decorator    
@app.callback()
def main(   
    version: Optional[bool] = typer.Option(
        None, #default value 
        "--version",
        "-v", #  set the command-line names for the version option: -v and --version.
        help="Show the version and exit.",
        callback=_version_callback, 
        is_eager=True
    )
) -> None:
    pass