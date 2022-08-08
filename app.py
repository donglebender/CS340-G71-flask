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
    # Separate out the request methods, in this case this is for a POST 
    # insert a person into the bsg_people entity
    if request.method == "POST":
        # fire off if user presses the Add Person button
        if request.form.get("Add_Person"):
            # grab user form inputs
            fname = request.form["fname"]
            lname = request.form["lname"]
            homeworld = request.form["homeworld"]
            age = request.form["age"]

            # account for null age AND homeworld
            if age == "" and homeworld == "0":
                # mySQL query to insert a new person into bsg_people with our form inputs
                query = "INSERT INTO bsg_people (fname, lname) VALUES (%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname))
                mysql.connection.commit()

            # account for null homeworld
            elif homeworld == "0":
                query = "INSERT INTO bsg_people (fname, lname, age) VALUES (%s, %s,%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, age))
                mysql.connection.commit()

            # account for null age
            elif age == "":
                query = "INSERT INTO bsg_people (fname, lname, homeworld) VALUES (%s, %s,%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, homeworld))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "INSERT INTO bsg_people (fname, lname, homeworld, age) VALUES (%s, %s,%s,%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, homeworld, age))
                mysql.connection.commit()

            # redirect back to people page
            return redirect("/people")



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



# route for delete functionality, deleting a person from bsg_people,
# we want to pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/delete_people/<int:id>")
def delete_people(id):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM bsg_people WHERE id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    # redirect back to people page
    return redirect("/people")

# route for edit functionality, updating the attributes of a person in bsg_people
# similar to our delete route, we want to the pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/edit_people/<int:id>", methods=["POST", "GET"])
def edit_people(id):
    if request.method == "GET":
        # mySQL query to grab the info of the person with our passed id
        query = "SELECT * FROM bsg_people WHERE id = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab planet id/name data for our dropdown
        query2 = "SELECT id, name FROM bsg_planets"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        homeworld_data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("edit_people.j2", data=data, homeworlds=homeworld_data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Person' button
        if request.form.get("Edit_Person"):
            # grab user form inputs
            id = request.form["personID"]
            fname = request.form["fname"]
            lname = request.form["lname"]
            homeworld = request.form["homeworld"]
            age = request.form["age"]

            # account for null age AND homeworld
            if (age == "" or age == "None") and homeworld == "0":
                # mySQL query to update the attributes of person with our passed id value
                query = "UPDATE bsg_people SET bsg_people.fname = %s, bsg_people.lname = %s, bsg_people.homeworld = NULL, bsg_people.age = NULL WHERE bsg_people.id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, id))
                mysql.connection.commit()

            # account for null homeworld
            elif homeworld == "0":
                query = "UPDATE bsg_people SET bsg_people.fname = %s, bsg_people.lname = %s, bsg_people.homeworld = NULL, bsg_people.age = %s WHERE bsg_people.id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, age, id))
                mysql.connection.commit()

            # account for null age
            elif age == "" or age == "None":
                query = "UPDATE bsg_people SET bsg_people.fname = %s, bsg_people.lname = %s, bsg_people.homeworld = %s, bsg_people.age = NULL WHERE bsg_people.id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, homeworld, id))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "UPDATE bsg_people SET bsg_people.fname = %s, bsg_people.lname = %s, bsg_people.homeworld = %s, bsg_people.age = %s WHERE bsg_people.id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, homeworld, age, id))
                mysql.connection.commit()

            # redirect back to people page after we execute the update query
            return redirect("/people")


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


@app.route('/customers', methods=["POST", "GET"])
def customers():

     # Separate out the request methods, in this case this is for a POST 
    # insert a person into the bsg_people entity
    if request.method == "POST":
        # fire off if user presses the Add Person button
        if request.form.get("Add_Customer"):
            # grab user form inputs
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            custEmail = request.form["custEmail"]

            # no null inputs
            query = "INSERT INTO Customers (firstName, lastName, custEmail) VALUES (%s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (firstName, lastName, custEmail))
            mysql.connection.commit()

            # redirect back to people page
            return redirect("/customers")

        # Grab bsg_people data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the people in bsg_people
        query = "SELECT customerID, firstName, lastName, custEmail FROM Customers;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("customers.j2", data=data)

# route for edit functionality, updating the attributes of a person in bsg_people
# similar to our delete route, we want to the pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/edit_customer/<int:customerID>", methods=["POST", "GET"])
def edit_customer(customerID):
    if request.method == "GET":
        # mySQL query to grab the info of the person with our passed id
        query = "SELECT * FROM Customers WHERE customerID = %s" % (customerID)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()


        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("edit_customer.j2", data=data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Person' button
        if request.form.get("Edit_Customer"):
            # grab user form inputs
            customerID = request.form["customerID"]
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            custEmail = request.form["custEmail"]


            query = "UPDATE Customers SET firstName = %s, lastName = %s, custEmail = %s WHERE customerID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (firstName, lastName, custEmail, customerID))
            mysql.connection.commit()

            # redirect back to people page after we execute the update query
            return redirect("/customers")

# route for delete functionality, deleting a person from bsg_people,
# we want to pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/delete_customer/<int:customerID>")
def delete_customer(customerID):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM Customers WHERE customerID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (customerID,))
    mysql.connection.commit()

    # redirect back to people page
    return redirect("/customers")


@app.route('/instructors', methods=["POST", "GET"])
def instructors():

     # Separate out the request methods, in this case this is for a POST 
     # insert an instructor
    if request.method == "POST":
        # fire off if user presses the Add Instructor button
        if request.form.get("Add_Instructor"):
            # grab user form inputs
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            instructEmail = request.form["instructEmail"]

            # no null inputs
            query = "INSERT INTO Instructors (firstName, lastName, instructEmail) VALUES (%s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (firstName, lastName, instructEmail))
            mysql.connection.commit()

            # redirect back to people page
            return redirect("/instructors")

        # Grab Instructors data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the people in Instructors
        query = "SELECT instructorID, firstName, lastName, instructEmail FROM Instructors;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render instructor page
        return render_template("instructors.j2", data=data)

@app.route("/edit_instructor/<int:instructorID>", methods=["POST", "GET"])
def edit_instructor(instructorID):
    if request.method == "GET":
        # mySQL query to grab the info of the person with our passed id
        query = "SELECT * FROM Instructors WHERE instructorID = %s" % (instructorID)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()


        # render edit_instructor
        return render_template("edit_instructor.j2", data=data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Instructor' button
        if request.form.get("Edit_Instructor"):
            # grab user form inputs
            instructorID = request.form["instructorID"]
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            instructEmail = request.form["instructEmail"]


            query = "UPDATE Instructors SET firstName = %s, lastName = %s, instructEmail = %s WHERE instructorID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (firstName, lastName, instructEmail, instructorID))
            mysql.connection.commit()

            # redirect back to Instructors page after we execute the update query
            return redirect("/instructors")

@app.route("/delete_instructor/<int:instructorID>")
def delete_instructor(instructorID):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM Instructors WHERE instructorID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (instructorID,))
    mysql.connection.commit()

    # redirect back to people page
    return redirect("/instructors")

@app.route('/lessons', methods=["POST", "GET"])
def lessons():
     # Separate out the request methods, in this case this is for a POST 
     # insert a lesson
    if request.method == "POST":
        # fire off if user presses the Add Lesson button
        if request.form.get("Add_Lesson"):
            # grab user form inputs
            instructorID = request.form["instructorID"]
            lessonType = request.form["lessonType"]
            lessonDate = request.form["lessonDate"]
            requestBool = request.form["request"]

            # no null inputs
            query = "INSERT INTO Lessons (instructorID, lessonType, lessonDate, request) VALUES (%s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (instructorID, lessonType, lessonDate, requestBool))
            mysql.connection.commit()

            # redirect back to people page
            return redirect("/lessons")

        # Grab Lessons data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the people in Instructors
        query = "SELECT * FROM Lessons;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("lessons.j2", data=data)

@app.route("/delete_lesson/<int:lessonID>")
def delete_lessons(lessonID):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM Lessons WHERE lessonID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (lessonID,))
    mysql.connection.commit()

    # redirect back to people page
    return redirect("/lessons")

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8021))
    app.run(port=port, debug=True) 