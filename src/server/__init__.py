from flask import Flask
from flask_socketio import SocketIO

app_server = Flask(
                __name__, 
               template_folder = "templates",
               static_folder="static",
               static_url_path=""
           )

socketio = SocketIO(app_server, async_mode="gevent", cors_allowed_origins="*")
socket_conns = {}

from src.task_manager import task_manager

from . import routes
