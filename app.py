# Imports
from flask import Flask, render_template, request
from flask_cors import CORS
import sqlite3 as sql

app = Flask(__name__, static_folder='static')
CORS(app)

@app.route("/")
def hello():
    return render_template('input.html')

@app.post("/api/sendMessage")
def doTheThing():
    data = request.json
    return data["message"]
