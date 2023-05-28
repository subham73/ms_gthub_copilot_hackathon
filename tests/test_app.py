"""unit tests for app.py using pytest"""
import pytest
from typer.testing import CliRunner 
from app import __version__, __app_name__, cli

# # create a fixture for the CliRunner() object
# @pytest.fixture()
# def runner():
#     return CliRunner()

# # create a fixture for the main() function
# @pytest.fixture()
# def main():
#     return cli.app(prog_name=__app_name__)

runner = CliRunner()
def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} version {__version__}\n" in result.stdout
