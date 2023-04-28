import os
import re
import sys
import json
import string
import mysql.connector
import random2 as random
from forms import LoginForm, AssignmentForm, EventForm
from datetime import timedelta
from flask import Flask, request, make_response, render_template, redirect, session, url_for

app = Flask(__name__, template_folder = 'templates', static_folder = 'static')

# SECRET_KEY = os.urandom(32)
# app.secret_key = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(random.randint(8, 16))])
app.permanent_session_lifetime = timedelta(minutes = 45)
# SECRET_KEY = os.environ.get('SECRET_KEY')
app.config['SECRET_KEY'] = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(random.randint(8, 16))])

sN = "MYVLE"
allCourses = ""
host = "localhost"
username = "COMP3161Group"
password = "tJ58FIU!uuV/3HS8"
database = "comp3161_final_project"

def connectToDB():
    conn = mysql.connector.connect(
        user = username,
        password = password,
        host = host,  
        database = database)

    cursor = conn.cursor()

    return conn, cursor

@app.route('/Event/<course_id>', methods = ['GET'])
def event(course_id):
    try:
        query = f"SELECT `Calender ID`, Name, Type, Description, Date, (SELECT `Course Name` FROM courses WHERE `Course ID` = {course_id!r}) FROM `Course Calenders` WHERE `Course Calenders`.`Course ID` = {course_id!r}"
        conn, cursor = connectToDB()
        eventLst = []
        cursor.execute(query)
        for eventID, eventName, eventType, eventDescription, eventDate, courseName in cursor:
            event = {} 
            event['Event ID'] = eventID
            event['Name'] = eventName
            event['Type'] = eventType
            event['Description'] = eventDescription
            event['Date'] = eventDate
            event['Course Name'] = courseName
            eventLst.append(event)
        conn.close()
        cursor.close()
        return make_response(eventLst, 200)
    except Exception as e:
        return make_response(str(e), 400)

@app.route('/Assignment/<course_id>', methods = ['GET'])
def assignments(course_id):
    try:
        query = f"SELECT `Assignment ID`, Name, Type, Description, `Start Date`, `End Date`, (SELECT `Course Name` FROM courses WHERE `Course ID` = {course_id!r}) FROM `Course Assignments` WHERE `Course Assignments`.`Course ID` = {course_id!r}"
        conn, cursor = connectToDB()
        assignmentLst = []
        cursor.execute(query)
        for assID, assName, assType, assDescip, start, end, courseName in cursor:
            assignment = {} 
            assignment['Assignment ID'] = assID
            assignment['Name'] = assName
            assignment['Type'] = assType
            assignment['Start Date'] = start
            assignment['End Date'] = end
            assignment['Description'] = assDescip
            assignment['Course Name'] = courseName
            assignmentLst.append(assignment)
        conn.close()
        cursor.close()
        return make_response(assignmentLst, 200)
    except Exception as e:
        return make_response(str(e), 400)

@app.route('/Courses', methods = ['GET'])
def courses():
    try:
        query = "SELECT * FROM Courses"
        conn, cursor = connectToDB()
        courseLst = []
        cursor.execute(query)
        for idNumber, courseName in cursor:
            course = {}
            course['Course ID'] = idNumber
            course['Course Name'] = courseName
            courseLst.append(course)
        conn.close()
        cursor.close()
        return make_response(courseLst, 200)
    except Exception as e:
        return make_response(str(e), 400)

@app.route('/CoursesByStudent/<student_id>', methods = ['GET'])
def courseByStudent(student_id):
    try:
        query = f"SELECT `Course Students`.`Course ID`, Courses.`Course Name` FROM `Course Students` RIGHT JOIN courses ON `Course Students`.`Course ID` = Courses.`Course ID` WHERE `Course Students`.`Student ID` = {student_id!r}"
        conn, cursor = connectToDB()
        courseLst = []
        cursor.execute(query)
        for courseID, courseName in cursor:
            course = {}
            course['Course ID'] = courseID
            course['Course Name'] = courseName
            courseLst.append(course)
        conn.close()
        cursor.close()
        return make_response(courseLst, 200)
    except Exception as e:
        return make_response(str(e), 400)

@app.route('/CoursesByLecturer/<lecturer_id>', methods = ['GET'])
def courseByLecturer(lecturer_id):
    try:
        query = f"SELECT `Course Lecturers`.`Course ID`, Courses.`Course Name` FROM `Course Lecturers` RIGHT JOIN courses ON `Course Lecturers`.`Course ID` = Courses.`Course ID` WHERE `Course Lecturers`.`Lecturer ID` = {lecturer_id!r}"
        conn, cursor = connectToDB()
        courseLst = []
        cursor.execute(query)
        for courseID, courseName in cursor:
            course = {}
            course['Course ID'] = courseID
            course['Course Name'] = courseName
            courseLst.append(course)
        conn.close()
        cursor.close()
        return make_response(courseLst, 200)
    except Exception as e:
        return str(e)

@app.route('/Login/<user_id>&<user_password>', methods = ['POST'])
def login(user_id, user_password):
    try:
        if(user_id[0] == "S"):
            query = f"SELECT * FROM Students WHERE `Student ID` = {user_id!r} AND Password = {user_password!r}"
        elif(user_id[0] == "L"):
            query = f"SELECT * FROM Lecturers WHERE `Lecturer ID` = {user_id!r} AND Password = {user_password!r}"
        else:
            query = f"SELECT * FROM Admins WHERE `Admin ID` = {user_id!r} AND Password = {user_password!r}"
        conn, cursor = connectToDB()
        loginStatus = ""
        cursor.execute(query)
        row = cursor.fetchone()
        if row is not None:
            if(user_id[0] == "S"):
                studentID, firstName, lastName, email, age, birthday, password = row
                student = {}
                student['Student ID'] = studentID
                student['First Name'] = firstName
                student['Last Name'] = lastName
                student['Email'] = email
                student['Age'] = age
                student['Birthday'] = birthday
                student['Password'] = password
                loginStatus = f"{firstName} {lastName} {studentID}"
            elif(user_id[0] == "L"):
                lecturerID, firstName, lastName, email, age, birthday, password = row
                lecturer = {}
                lecturer['Lecturer ID'] = lecturerID
                lecturer['First Name'] = firstName
                lecturer['Last Name'] = lastName
                lecturer['Email'] = email
                lecturer['Age'] = age
                lecturer['Birthday'] = birthday
                lecturer['Password'] = password
                loginStatus = f"{firstName} {lastName} {lecturerID}"
            else:
                adminID, firstName, lastName, email, age, birthday, password = row
                admin = {}
                admin['Admin ID'] = adminID
                admin['First Name'] = firstName
                admin['Last Name'] = lastName
                admin['Email'] = email
                admin['Age'] = age
                admin['Birthday'] = birthday
                admin['Password'] = password
                loginStatus = f"{firstName} {lastName} {adminID}"                
            return make_response(loginStatus, 200)
        else:
            return make_response("User not found", 200)
    except Exception as e:
        return make_response(str(e), 400)

@app.route('/Course/addEvent/<course_id>', methods = ['GET'])
def addEvent(course_id):
    try:
        query = "SELECT COUNT(`Calender ID`) FROM `Course Calenders`"
        conn, cursor = connectToDB()
        content = request.json
        eventName = content['Event Name']
        eventType = content['Event Type']
        eventDate = content['Event Date']
        eventDescription = content['Event Description']
        cursor.execute(query)
        rowCount = cursor.fetchone()[0]
        query = f"INSERT INTO `Course Calenders` VALUES('CE{rowCount}', {eventName!r}, {eventType!r}, {eventDescription!r}, {eventDate!r}, {course_id!r})"
        cursor.execute(query)
        conn.commit()
        conn.close()
        cursor.close()
        return make_response({'Success': 'Calender Event Added'}, 200)
    except Exception as e:
        return(str(e))

@app.route('/Course/addAssignment/<course_id>', methods = ['GET'])
def addAssignment(course_id):
    try:
        query = "SELECT COUNT(`Assignment ID`) FROM `Course Assignments`"
        conn, cursor = connectToDB()
        content = request.json
        assignmentName = content['Assignment Name']
        assignmentType = content['Assignment Type']
        assignmentDescription = content['Assignment Description']
        assignmentStartDate = content['Assignment Start Date']
        assignmentDueDate = content['Assignment Due Date']
        cursor.execute(query)
        rowCount = cursor.fetchone()[0]
        query = f"INSERT INTO `Course Assignments` VALUES('CA{rowCount}', {assignmentName!r}, {assignmentType!r}, {assignmentDescription!r}, {assignmentStartDate!r}, {assignmentDueDate!r}, {course_id!r})"
        cursor.execute(query)
        conn.commit()
        conn.close()
        cursor.close()
        return make_response({'Success': 'Assignment Added'}, 200)
    except Exception as e:
        return(str(e))
    # return render_template("addEvent.html", form = form, course_id = course_id)

def toList(func):
    word = func().data
    word = str(word, 'utf-8')
    word = " ".join(word.split()).strip("[]").replace('" ', '"').replace(' "', '"')
    
    tmpLst = []
    temp = ""

    for index, let in enumerate(word):
        if let == "{":
            temp = let
        elif ((let == "," and word[index-1] == "}") or len(word)-1 == index):
            tmpLst.append(json.loads(temp))
        elif let != "{" or let != "}":
            temp += let
    return tmpLst

@app.route(f'/{sN}/course/addEvent/<course_id>', methods = ['GET', 'POST'])
def addEventPage(course_id):
    form = EventForm()
    if form.validate_on_submit():
        try:
            query = "SELECT COUNT(`Calender ID`) FROM `Course Calenders`"
            conn, cursor = connectToDB()
            eventName = request.form['eventName']
            eventType = request.form['eventType']
            eventDescription = request.form['eventDescription']
            eventDate = request.form['eventDate']
            cursor.execute(query)
            rowCount = cursor.fetchone()[0]
            query = f"INSERT INTO `Course Calenders` VALUES('CE{rowCount}', {eventName!r}, {eventType!r}, {eventDescription!r}, {eventDate!r}, {course_id!r})"
            cursor.execute(query)
            conn.commit()
            conn.close()
            cursor.close()
            return render_template("addEvent.html", form = form, message = "Calender Event Added")
        except Exception as e:
            return(str(e))      
    return render_template("addEvent.html", form = form, course_id = course_id)

@app.route(f'/{sN}/course/addAssignment/<course_id>', methods = ['GET', 'POST'])
def addAssignmentPage(course_id):
    form = AssignmentForm()
    if form.validate_on_submit():
        try:
            print("asd")
            query = "SELECT COUNT(`Assignment ID`) FROM `Course Assignments`"
            conn, cursor = connectToDB()
            assignmentName = request.form['assignmentName']
            assignmentType = request.form['assignmentType']
            assignmentDescription = request.form['assignmentDescription']
            assignmentStartDate = request.form['assignmentStartDate']
            assignmentDueDate = request.form['assignmentDueDate']
            cursor.execute(query)
            rowCount = cursor.fetchone()[0]
            query = f"INSERT INTO `Course Assignments` VALUES('CA{rowCount}', {assignmentName!r}, {assignmentType!r}, {assignmentDescription!r}, {assignmentStartDate!r}, {assignmentDueDate!r}, {course_id!r})"
            cursor.execute(query)
            conn.commit()
            conn.close()
            cursor.close()
            return render_template("addAssignment.html", form = form, message = "Assignment Added")
        except Exception as e:
            return(str(e))
    return render_template("addAssignment.html", form = form, course_id = course_id)
#IMPLEMENTATION NEEDED
@app.route(f'/{sN}/course/<event>', methods = ['GET'])
def calenderPage(event):
    event = event.replace("'", '"')
    event = json.loads(event)
    return render_template("calender.html", event = event)

@app.route(f'/{sN}/assignment/<assignment>', methods = ['GET'])
def assignmentPage(assignment):
    assignment = assignment.replace("'", '"')
    assignment = json.loads(assignment)
    return render_template("assignment.html", assignment = assignment)

@app.route(f'/{sN}/home', methods = ['GET'])
def homePage():
    if session.get('logged_in') == True:
        return render_template("home.html", courses = session['courses'])
    else:
        session['user'] = "Guest"
        session['courses'] = toList(lambda: courses())
        return render_template("home.html", courses = session['courses'])

@app.route(f'/{sN}/login', methods = ['GET', 'POST'])
def loginPage():
    form = LoginForm()
    if form.validate_on_submit():
        loginStatus = login(request.form['username'], request.form['password']).data
        loginStatus = str(loginStatus, 'utf-8')
        if loginStatus == "User not found":
            return render_template("login.html", form = form, message = "User not found")
        else:
            session.permanent = True
            loginStatus = loginStatus.split()
            if loginStatus[2][0] == "S":
                studentCourses = toList(lambda: courseByStudent(loginStatus[2]))
                session['courses'] = studentCourses
                session['user'] = loginStatus[0] + " " +loginStatus[1]
                session['logged_in'] = True
                session['type'] = "Student"
                session['id'] = loginStatus[2]
                session.modified = True
                return redirect(url_for("homePage"))
            elif loginStatus[2][0] == "L":
                LecturerCourses = toList(lambda: courseByLecturer(loginStatus[2]))
                session['courses'] = LecturerCourses
                session['user'] = loginStatus[0] + " " +loginStatus[1]
                session['logged_in'] = True
                session['type'] = "Lecturer"
                session['id'] = loginStatus[2]
                session.modified = True
                return redirect(url_for("homePage"))                
            else:
                adminCourses = toList(lambda: courses())
                session['courses'] = adminCourses
                session['user'] = loginStatus[0] + " " +loginStatus[1]
                session['logged_in'] = True
                session['type'] = "Admin"
                session['id'] = loginStatus[2]
                session.modified = True
                return redirect(url_for("homePage"))
    else:
        return render_template("login.html", form = form, message = "")

@app.route(f'/{sN}/logout', methods = ['GET'])
def logout():
    session.clear()
    app.config['SECRET_KEY'] = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(random.randint(8, 16))])
    return redirect(url_for('landingPage'))

@app.route(f'/{sN}', methods = ['GET'])
def landingPage():
    if session.get('logged_in') == True:
        return render_template("home.html", courses = session['courses'])
    else:
        return redirect(url_for("loginPage"))

@app.route(f'/{sN}/course/<course_id>&<course_name>', methods = ['GET'])
def coursePage(course_id, course_name):
    courseCalenders = toList(lambda: event(course_id))
    courseAssignments = toList(lambda: assignments(course_id))
    return render_template("coursePage.html", course_id = course_id, course_name = course_name, calender = courseCalenders, assignments = courseAssignments)

if __name__ == 'main':
    app.run()