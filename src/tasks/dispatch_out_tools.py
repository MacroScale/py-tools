import asyncio 

from src.config.db import SQLiteDB 
from src.utils.get_local_tools import get_local_tools
import src.queries.sync_tools as query_sync_tools
from src.task_manager.task_manager import task_manager

from src.server import socketio

from src.server import socket_conns 

async def dispatch_out_tools():
    """ used to dispatch the output of a tool to corresponding socket """
    while True:
        #iterate over a copy of the keys
        for id in list(task_manager.tasks.keys()): 
            task_info = task_manager.get_task_info(id)
            if not task_info: continue

            # process output
            out = task_manager.get_output(id)
            if id in socket_conns:
                session_id = socket_conns[id]
                socketio.emit('stream', {"stream_data": out}, to=session_id)
                # will delete if finished
                task_manager.delete_task(id)

        await asyncio.sleep(0.15)
