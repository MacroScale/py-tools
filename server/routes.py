from . import app_server
from flask import render_template

@app_server.route("/")
def index():
    return render_template("index.html")
