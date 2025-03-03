from shared_utils.db import SQLiteDB 

def run(db: SQLiteDB):
    statement = """
        SELECT * from scripts
    """
    result = db.execute(statement)
    return result
