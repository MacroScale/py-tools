from src.config.db import SQLiteDB 
from src.models.tool import Tool 

def run(db: SQLiteDB) -> list[Tool]:
    statement = """
        SELECT * from scripts
    """
    resp = db.execute(statement)

    result = []
    for el in resp:
        result.append(Tool.MapTuple(el));

    return result
