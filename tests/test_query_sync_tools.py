import pytest
import datetime 
from src.utils.get_local_tools import get_local_tools
import src.queries.sync_tools as query_sync
import src.queries.get_tools as query_get_tools
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

def test_query_sync_remove():
    td_tools = ['tool_1.py', 'tool_2.py', 'tool_3.py', 'tool_4.py']
    db = SQLiteDB(test=True)

    query_sync.run(db, td_tools)
    new_tools = query_get_tools.run(db)

    # checks if remove old it removed 
    assert new_tools == [
            Tool(2, 'tool_1.py', 'not_running', None, None),
            Tool(3, 'tool_2.py', 'not_running', None, None), 
            Tool(4, 'tool_3.py', 'not_running', None, None), 
            Tool(5, 'tool_4.py', 'not_running', None, None)
        ]

def test_query_sync_remove_and_persist():
    td_tools = ['tool_1.py', 'tool_2.py', 'test_tool_1.py', 'tool_4.py']
    db = SQLiteDB(test=True)

    query_sync.run(db, td_tools)
    new_tools = query_get_tools.run(db)

    assert new_tools == [
            Tool(1, 'test_tool_1.py', 'not_running', 'complete', '2025-03-03T00:00:00'), 
            Tool(2, 'tool_1.py', 'not_running', None, None),                             
            Tool(3, 'tool_2.py', 'not_running', None, None),                             
            Tool(4, 'tool_4.py', 'not_running', None, None)                              
         ]
