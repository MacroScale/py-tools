import os
import time 

from src.task_manager.task_manager import task_manager 
from src.utils.get_local_tools import get_local_tools

def test_start_task_stdout():
    tool_path = os.path.abspath("tools/test_tool.py")
    assert os.path.exists(tool_path)

    task_manager.start_task(tool_path, 1)
    time.sleep(1)
    
    out = task_manager.get_output(1)
    stdout = out["stdout"]

    print(stdout)

    task_manager.stop_task(1)

    assert stdout
