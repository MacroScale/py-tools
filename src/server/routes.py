from . import app_server, socketio
from flask import render_template

from src.config.db import SQLiteDB 
import src.queries.get_tools as query_get_tools

@app_server.route("/")
def index():
    db = SQLiteDB()
    tool_data = query_get_tools.run(db)
    return render_template("index.html", tools=tool_data)

@socketio.on('connect')
def handle_connect():
    print('Client connected')
