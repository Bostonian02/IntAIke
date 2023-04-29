# Imports
from flask import Flask
from flask_cors import CORS
import sqlite3 as sql

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    try:
        my_list = []
        # Connect to the database
        con = sql.connect('Cases.db')

        # Get the cursor
        c = con.cursor()

        #Add data
        cursor = c.execute("SELECT NAME FROM CASES")
        for row in cursor:
            my_list.append(row)

        con.close()

        return my_list
    except Exception as e:
        return e
