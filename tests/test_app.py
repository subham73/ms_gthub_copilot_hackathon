"""unit tests for app.py using pytest"""
import pytest
from typer.testing import CliRunner 
import json

from app import (
    DB_READ_ERROR,
    SUCCESS,
    __app_name__,
    __version__,
    cli,
    app,
)

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

@pytest.fixture
def mock_json_file(tmp_path):
    todo = ["paradip"]
    db_file = tmp_path / "todo.json"
    with db_file.open("w") as db:
        json.dump(todo, db, indent=4)
    return db_file

# test_data1 = "Delhi"
# test_data2 = "Bhubaneswar"

# pytest.mark.parametrize(
#     # "city",
#     [
#         pytest.param(
#             test_data1,
#             ("Delhi", SUCCESS),
#         ),
#         pytest.param(
#             test_data2,
#             ("Bhubaneswar", SUCCESS),
#         ),
#     ],
# )
# def test_add(mock_json_file, city, expected):
#     todoer = app.Todoer(mock_json_file)
#     assert todoer.add(city) == expected
#     read = todoer._db_handler.read_todos()
#     assert len(read.todo_list) == 2


