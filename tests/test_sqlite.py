import pytest 
import datetime
from src.config.db import SQLiteDB 

@pytest.fixture(scope="module", autouse=True)
def test_data():
    db = SQLiteDB(test=True);
    db.clear_db_data()

    statement = """
        INSERT INTO scripts (name, execution_status, exit_status, last_run)
        VALUES (:name, :execution_status, :exit_status, :last_run);
    """
    data = {
        "name": "test_tool_1.py",
        "execution_status": "not_running",
        "exit_status": "complete",
        "last_run": datetime.datetime(2025, 3, 3, 0, 0).isoformat(),
    }

    db.execute(statement, [data])


def test_basic_statement():
    db = SQLiteDB(test=True);
    result = db.execute("SELECT * FROM scripts;")
    expected = [(1, 'test_tool_1.py', 'not_running', 'complete', '2025-03-03T00:00:00')]
    assert result == expected
    
