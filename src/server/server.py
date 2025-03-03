from . import app_server, socketio

import asyncio
from threading import Thread

def run_server():
    socketio.run(app_server, host="0.0.0.0", port=8080, debug=True, use_reloader=False)

async def Start():
    server_thread = Thread(target=run_server, daemon=True)
    # allow the program to exit even if the thread is running
    server_thread.start()
    
    # keep the async function alive
    while True:
        await asyncio.sleep(1)
