# Imports
from flask import Flask, render_template, request
from flask_cors import CORS
import sqlite3 as sql
import random
import sys
from MonetaryValueBot import get_monetary_value

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

def write_client_info(FirstName, LastName, BirthDate, SocialSecurity, Address, ZipCode, Email, PhoneNumber, Insured, InsuranceName, InsuranceGroupNum, InsuranceMemberID):
    Client_ID = random.randint(1, 100000000)
    connection = sql.connect('Intakes.db')
    cursor = connection.cursor()
    is_insured = 1 if Insured == "on" else 0
    sql_query = f'INSERT INTO CLIENTS(Client_ID, First_Name, Last_Name, Social_Security_Number, Date_of_Birth, Home_Address, Zip_Code, Email_Address, Phone_Number, ID_Picture, Insured, Insurance_Memeber_ID, Insurance_Group_Number, Insurance_Company_Name, Insurance_Card_Picture) VALUES ({Client_ID}, \'{FirstName}\', \'{LastName}\', \'{SocialSecurity}\', \'{BirthDate}\', \'{Address}\', \'{ZipCode}\', \'{Email}\', \'{PhoneNumber}\', null, {is_insured}, \'{InsuranceMemberID}\', \'{InsuranceGroupNum}\', \'{InsuranceName}\', null);'
    cursor.execute(sql_query)
    connection.commit()
    cursor.close()
    connection.close()

def pick_response():
    respones = ["Hello I am real Chatbot", "You are definitely talking to a chat bot right now (wink wink)", "What up, it's Automated CJ"]
    return (random.choice(respones))

@app.route("/")
def hello():
    return render_template('input.html')

@app.route("/referrals")
def goodbye():
    return render_template('referrals.html')

@app.route("/inputForm")
def showInput():
    return render_template('inputForm.html')

@app.route("/chat")
def showChat():
    FirstName = request.args.get('FirstName')
    LastName = request.args.get('LastName')
    BirthDate = request.args.get('BirthDate')
    SocialSecurity = request.args.get('SocialSecurity')
    Address= request.args.get('Address')
    ZipCode = request.args.get('ZipCode')
    Email = request.args.get('Email')
    PhoneNumber = request.args.get('PhoneNumber')
    Insured = request.args.get('InsuredCheck')
    InsuranceName = request.args.get('InsuranceName')
    InsuranceGroupNum = request.args.get('InsuranceGroupNum')
    InsuranceMemberID = request.args.get('InsuranceMemberID')
    write_client_info(FirstName, LastName, BirthDate, SocialSecurity, Address, ZipCode, Email, PhoneNumber, Insured, InsuranceName, InsuranceGroupNum, InsuranceMemberID)
    return render_template('chat.html')

# API endpoints
@app.post("/api/sendMessage")
def doTheThing():
    data = request.json
    return pick_response()

@app.post("/api/clientInput")
def giveData():
    data = request.data
    print(data, file=sys.stderr)
    return data

@app.post("/api/monetaryValue")
def doAIStuff():
    data = request.json
    return get_monetary_value(data["case_type"])
