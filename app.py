import os
import re
import sys
import string
import mysql.connector
import random2 as random
from forms import LoginForm
from datetime import timedelta
from flask import Flask, request, make_response, render_template, redirect, session, url_for

app = Flask(__name__)

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
        print(str(e))

@app.route('/login/<user_id>&<user_password>', methods = ['POST'])
def login(user_id, user_password):
    try:
        if(user_id[0] == "S"):
            query = f"SELECT * FROM Students WHERE `Student ID` = {user_id!r} AND Password = {user_password!r}"
        else:
            query = f"SELECT * FROM Lecturers WHERE `Lecturer ID` = {user_id!r} AND Password = {user_password!r}"
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
            else:
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
            return make_response(loginStatus, 200)
        else:
            return make_response("User not found", 200)
    except Exception as e:
        return make_response(str(e), 400)

def toList(func):
    word = func().data
    word = str(word, 'utf-8')
    word = word.replace("},", "}!").replace("\n", "")

    word = word.split("!")
    word = [l for l in word if l != ","]
    for index, item in enumerate(word):

        word[index] = item.split(",")
        word[index][0] = word[index][0][4:]
        word[index][1] = word[index][1][:-3]    
    return word

@app.route(f'/{sN}/home')
def homePage():
    if session.get('logged_in') == True:
        if session['type'] == "Student":
            studentCourses = toList(lambda: courseByStudent(session['id']))
            return render_template("home.html")
        # elif session['type'] == "Lecturer":
    else:
        session['user'] = "Guest"
        allCourses = toList(lambda: courses())
        return render_template("home.html", courses = allCourses)

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
                print(loginStatus, file=sys.stderr)
                session.modified = True
                return redirect(url_for("homePage"))
            # return render_template("home.html", )
        # return redirect("home.html", user = )
    # print(loginStatus, file=sys.stderr)
    # if form.validate_on_submit():
    #     return "asd"
    else:
        return render_template("login.html", form = form, message = "")

@app.route(f'/{sN}/logout')
def logout():
    session.clear()
    app.config['SECRET_KEY'] = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(random.randint(8, 16))])
    return redirect(url_for('landingPage'))

@app.route(f'/{sN}')
def landingPage():
    if session.get('logged_in') == True:
        return render_template("home.html", courses = session['courses'])
    else:
        return redirect(url_for("loginPage"))

if __name__ == 'main':
    app.run()