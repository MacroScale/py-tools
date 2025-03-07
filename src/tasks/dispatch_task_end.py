from src.task_manager.task_manager import task_manager
from src.server import socketio
from src.server import socket_conns 

import asyncio 

async def dispatch_task_end():
    """ used to dispatch the output of a tool to corresponding socket """
    prev_task_ids = list(task_manager.tasks.keys()); 
    while True:
        for id in prev_task_ids: 
            task_info = task_manager.get_task_info(id)
            if not task_info: 
                if id in socket_conns:
                    session_id = socket_conns[id]
                    socketio.emit('task_end', {"task_id": id}, to=session_id)
        prev_task_ids = list(task_manager.tasks.keys()); 
        await asyncio.sleep(0.15)
