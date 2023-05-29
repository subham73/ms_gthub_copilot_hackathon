# commnad line tool using typer
from pathlib import Path
from typing import Optional
import typer

# from __inti__.py import __version__ and __app_name__
from . import __version__, __app_name__, config, database

# create command line interface using typer
app = typer.Typer()

@app.command()
def init(
    db_path: str = typer.Option(
        str(database.DEFAULT_DB_FILE_PATH),
        "--db-path",
        "-db",
        prompt="to-do database location?",
    ),
) -> None:
    """Initialize the to-do database."""
    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(
            f'Creating config file failed with "{ERRORS[app_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho( # typer.secho() allows you to use different colors when printing text to the screen
            f'Creating database failed with "{ERRORS[db_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The to-do database is {db_path}", fg=typer.colors.GREEN)

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