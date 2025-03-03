from . import app_server
from flask import render_template

from shared_utils.db import SQLiteDB 

@app_server.route("/")
def index():
    db = SQLiteDB();
    return render_template("index.html")
