from . import app_server, socketio

def Start():
    print("Starting server on port 8080...")
    socketio.run(app_server, host="0.0.0.0", port=8080)
