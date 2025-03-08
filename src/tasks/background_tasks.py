import gevent
from src.tasks.update_tool_scripts import update_tools_files
from src.tasks.dispatch_out_tools import dispatch_out_tools

def Start():
    greenlets = [
        gevent.spawn(update_tools_files),
        gevent.spawn(dispatch_out_tools),
    ]
    gevent.joinall(greenlets)
