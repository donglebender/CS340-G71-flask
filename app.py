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

    # Write the query and save it to a variable
    query = "SELECT * FROM bsg_people;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("bsg.j2", bsg_people=results)

@app.route('/certifications')
def certs():
    return render_template("certifications.j2")

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
    port = int(os.environ.get('PORT', 8028))
    app.run(port=port, debug=True) 