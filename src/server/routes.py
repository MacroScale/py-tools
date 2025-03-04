from . import app_server, socketio, socket_conns
from flask import render_template, jsonify, request

from src.config.db import SQLiteDB 
import src.queries.get_tools as query_get_tools
import src.queries.get_tool_path as query_get_tool_path
from src.task_manager.task_manager import task_manager

@app_server.route("/")
def index():
    db = SQLiteDB()
    tool_data = query_get_tools.run(db)
    
    task_ids = [tool.id for tool in tool_data] 
    output_data = {id: task_manager.get_output(id) for id in task_ids}

    return render_template("index.html", tools=tool_data, output_data=output_data)

@app_server.route("/api/start/<int:tool_id>", methods=["GET"])
def api_start_task(tool_id):
    db = SQLiteDB()
    tool_path = query_get_tool_path.run(db, tool_id)
    task_manager.start_task(tool_path, tool_id)
    
    return jsonify(status=200, task_id=tool_id)

@socketio.on('connect')
def handle_connect():
    id = int(request.args.get('id'))
    session_id = request.sid
    print(f"Client connected with id: {id}, session_id: {session_id}")
    socket_conns[id] = session_id

@socketio.on('disconnect')
def handle_disconnect():
    id = int(request.args.get('id'))
    del socket_conns[id]

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)
