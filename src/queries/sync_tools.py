from shared_utils.db import SQLiteDB 

def run(db: SQLiteDB, tools: list[str]):
    stmt1 = """
        INSERT INTO scripts (name)
        SELECT :tool
        WHERE NOT EXISTS (
            SELECT 1 FROM scripts WHERE name = :tool
        );
    """
    stmt1_data = [{"tool": tool} for tool in tools]
    db.execute(stmt1, stmt1_data)

    if tools:
        # explode tool list
        placeholders = ", ".join(f":p{i}" for i in range(len(tools)))  
        stmt2 = f"""
            DELETE FROM scripts
            WHERE name NOT IN ({placeholders});
        """
        stmt2_data = {f"p{i}": tools[i] for i in range(len(tools))}
        db.execute(stmt2, stmt2_data)
