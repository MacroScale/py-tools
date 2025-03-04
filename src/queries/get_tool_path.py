from src.config.db import SQLiteDB 
from src.models.tool import Tool 
import os

def run(db: SQLiteDB, tool_id: int) -> str:
    statement = """
        SELECT * from scripts
        WHERE id = :tool_id
    """
    resp = db.execute(statement, {"tool_id": tool_id})

    result = []
    for el in resp:
        result.append(Tool.MapTuple(el));

    tool_name = result[0].name
    rel_path = f"tools/{tool_name}"
    tool_path = os.path.abspath(rel_path)

    return tool_path 
