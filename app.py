# Imports
from flask import Flask, render_template
from flask_cors import CORS
import sqlite3 as sql

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

@app.route("/")
# def hello_world():
#     try:
#         my_list = []
#         # Connect to the database
#         con = sql.connect('Cases.db')

#         # Get the cursor
#         c = con.cursor()

#         #Add data
#         cursor = c.execute("SELECT NAME FROM CASES")
#         for row in cursor:
#             my_list.append(row)

#         con.close()

#         return my_list
#     except Exception as e:
#         return e
def hello():
    return render_template('input.html')

@app.route("/referrals")
def display():
    return render_template('referrals.html')
