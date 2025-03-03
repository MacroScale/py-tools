import pytest
import datetime 
import src.queries.get_tools as query
from src.models.tool import Tool
from src.config.db import SQLiteDB 

@pytest.fixture(scope="function", autouse=True)
def init_test_data():
    db = SQLiteDB(test=True);
    db.clear_db_data()

    stmt1 = """
        INSERT INTO scripts (name, execution_status, exit_status, last_run)
        VALUES (:name, :execution_status, :exit_status, :last_run);
    """
    stmt1_data = {
        "name": "test_tool_1.py",
        "execution_status": "not_running",
        "exit_status": "complete",
        "last_run": datetime.datetime(2025, 3, 3, 0, 0).isoformat(),
    }

    db.execute(stmt1, stmt1_data)

def test_query_get_tools():
    db = SQLiteDB(test=True)
    tools = query.run(db)
    print(tools)

    assert tools == [Tool(1, 'test_tool_1.py', 'not_running', 'complete', '2025-03-03T00:00:00')]
