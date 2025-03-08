from src.config.db import SQLiteDB 
from src.utils.get_local_tools import get_local_tools
import src.queries.sync_tools as query_sync_tools

import gevent

def update_tools_files():
    db = SQLiteDB()
    while True:
        tool_data = get_local_tools()
        query_sync_tools.run(db, tool_data)
        gevent.sleep(300) # 5 mins
