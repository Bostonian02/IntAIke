# Imports
from flask import Flask, render_template, request
from flask_cors import CORS
import sqlite3 as sql
import random

app = Flask(__name__, static_folder='static')
CORS(app)

def pick_response():
    respones = ["Hello I am real Chatbot", "You are definitely talking to a chat bot right now (wink wink)", "What up, it's Automated CJ"]
    return (random.choice(respones))

@app.route("/")
def hello():
    return render_template('input.html')

@app.post("/api/sendMessage")
def doTheThing():
    data = request.json
    return pick_response()
