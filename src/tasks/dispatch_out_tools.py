from src.task_manager.task_manager import task_manager
from src.server import socketio
from src.server import socket_conns 

import gevent

def dispatch_out_tools():
    """ used to dispatch the output of a tool to corresponding socket """
    while True:
        # iterate over a copy of the tasks ids 
        for id in list(task_manager.tasks.keys()): 
            task_info = task_manager.get_task_info(id)
            if not task_info: continue

            # process output
            out = task_manager.get_output(id)
            status = task_manager.get_status(id)
            if id in socket_conns:
                session_id = socket_conns[id]
                socketio.emit('stream', {"out": out, "status": status}, to=session_id)
        gevent.sleep(0.2)
