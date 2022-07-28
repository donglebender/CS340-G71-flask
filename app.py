from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os
import database.db_connector as db

# Configuration

app = Flask(__name__)

db_connection = db.connect_to_database()

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_benderd'
app.config['MYSQL_PASSWORD'] = '8981' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_benderd'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

# Routes 

@app.route('/')
def root():
    return render_template("main.j2")

@app.route('/bsg-people')
def bsg_people():
    return "This is the bsg-people route."


@app.route('/people', methods=["POST", "GET"])
def people():
    # Grab bsg_people data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the people in bsg_people
        query = "SELECT bsg_people.id, fname, lname, bsg_planets.name AS homeworld, age FROM bsg_people LEFT JOIN bsg_planets ON homeworld = bsg_planets.id"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab planet id/name data for our dropdown
        query2 = "SELECT id, name FROM bsg_planets"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        homeworld_data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("people.j2", data=data, homeworlds=homeworld_data)


    # Write the query and save it to a variable
    #query = "SELECT * FROM bsg_people;"
    #cursor = db.execute_query(db_connection=db_connection, query=query)
    #results = cursor.fetchall()
    #return render_template("bsg.j2", bsg_people=results)

@app.route('/certifications', methods=["POST", "GET"])
def certs():
     # Grab bsg_people data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the people in bsg_people
        query = "SELECT certID, certName AS Certification FROM Certifications;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("certifications.j2", data=data)


@app.route('/customers')
def customers():
    return render_template("customers.j2")

@app.route('/instructors')
def instructors():
    return render_template("instructors.j2")

@app.route('/lessons')
def lessons():
    return render_template("lessons.j2")

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8021))
    app.run(port=port, debug=True) 