# Imports
from flask import Flask, render_template, request
from flask_cors import CORS
import sqlite3 as sql
import random
import sys
from MonetaryValueBot import get_monetary_value
from TrialBot import get_trial_prob

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

def write_client_info(FirstName, LastName, BirthDate, SocialSecurity, Address, ZipCode, Email, PhoneNumber, Insured, InsuranceName, InsuranceGroupNum, InsuranceMemberID):
    Client_ID = 517
    C_ID = Client_ID
    connection = sql.connect('Intakes.db')
    cursor = connection.cursor()
    is_insured = 1 if Insured == "on" else 0
    sql_query = f'INSERT INTO Clients(Client_ID, First_Name, Last_Name, Social_Security_Number, Date_of_Birth, Home_Address, Zip_Code, Email_Address, Phone_Number, ID_Picture, Insured, Insurance_Memeber_ID, Insurance_Group_Number, Insurance_Company_Name, Insurance_Card_Picture) VALUES ({Client_ID}, \'{FirstName}\', \'{LastName}\', \'{SocialSecurity}\', \'{BirthDate}\', \'{Address}\', \'{ZipCode}\', \'{Email}\', \'{PhoneNumber}\', null, {is_insured}, \'{InsuranceMemberID}\', \'{InsuranceGroupNum}\', \'{InsuranceName}\', null);'
    cursor.execute(sql_query)
    connection.commit()
    cursor.close()
    connection.close()

def write_incident_info(Description, Case_Type, Date, Time, Location, Zip_Code, Client_Role, Police_Report, Police_Case_Number, Medical_Visits, Pain_Scale, Inability_Type):
    Incident_ID = random.randint(1, 100000000)
    connection = sql.connect('Intakes.db')
    cursor = connection.cursor()
    is_reported = 1 if Police_Report == 'on' else 0
    sql_query = f'INSERT INTO Incidents(Incident_ID, Description, Case_Type, Date, Time, Location, Zip_Code, Client_Role, Police_Report, Police_Case_Number, Medical_Visits, Pain_Scale, Inability_Type, Client_ID) VALUES ({Incident_ID}, \'{Description}\', \'{Case_Type}\', \'{Date}\', \'{Time}\', \'{Location}\', \'{Zip_Code}\', \'{Client_Role}\', {is_reported}, \'{Police_Case_Number}\', {Medical_Visits}, {Pain_Scale}, \'{Inability_Type}\', 517);'
    cursor.execute(sql_query)
    connection.commit()
    cursor.close()
    connection.close()

def get_data_from_db(client_id):
    connection = sql.connect('Intakes.db')
    cursor = connection.cursor()
    sql_query = f'SELECT * FROM INCIDENTS WHERE Client_ID = {client_id}'
    cursor.execute(sql_query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

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
    return render_template('chat.html')

@app.route("/eval")
def showEval():
    if (not bool(request.args)):
        return render_template('eval.html')
    elif ('ClientID' in request.args):
        return render_template('eval.html')
    Case_Type = request.args.get('caseType')
    Description = request.args.get('IncidentDescription')
    Date = request.args.get('IncidentDate')
    Time = request.args.get('IncidentTime')
    Location = request.args.get('IncidentLocation')
    Zip_Code = request.args.get('IncidentZip')
    Client_Type = 'Plaintiff'
    Police_Report = request.args.get('PoliceInsured')
    Police_Case_Number = request.args.get('CaseNumber')
    Medical_Visits = request.args.get('MedVisit')
    Pain_Scale = request.args.get('PainScale')
    Inability_Type = request.args.get('NegativeAffects')
    write_incident_info(Description, Case_Type, Date, Time, Location, Zip_Code, Client_Type, Police_Report, Police_Case_Number, Medical_Visits, Pain_Scale, Inability_Type)
    return render_template('eval.html')

@app.route("/incidentForm")
def showIncForm():
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
    return render_template('incidentForm.html')

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

@app.post("/api/getIncidentData")
def getIncident():
    data = request.json
    client_id = data["id"]
    response = get_data_from_db(client_id)
    case_type = response[0][2]
    return case_type

@app.post("/api/getTrialProb")
def getProb():
    data = request.json
    return get_trial_prob(data["case_type"])
