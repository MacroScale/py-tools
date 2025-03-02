from . import app_server

def Start():
    app_server.run(host="0.0.0.0", port=8080, debug=True)
