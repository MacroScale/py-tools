import pytest
import datetime 
import src.queries.get_tool_path as query
from src.models.tool import Tool
from src.config.db import SQLiteDB 

import os


def test_get_tool_path():
    db = SQLiteDB()
    path = query.run(db, 5)
    print(path)

    assert path == os.path.abspath("tools/test_tool.py")
