import os
import re
import sys
import json
import string
import mysql.connector
import random2 as random
from datetime import timedelta, date
from forms import LoginForm, AssignmentForm, EventForm, AddUser, AddCourse
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

def availUsers(userType, lst):
    try:
        conn, cursor = connectToDB()
        userLst = []
        lst = tuple(lst)
        if userType == "Student":
            query = f"SELECT `Student ID` FROM `Course Students`GROUP BY `Student ID` HAVING `Student ID` IN {lst} AND COUNT(`STUDENT ID`) < 6"
            cursor.execute(query)
            for studID in cursor:
                student = {}
                student['Student ID'] = studID
                userLst.append(student)
            conn.close()
            cursor.close()
        elif userType == "Lecturer":
            query = f"SELECT `Lecturer ID` FROM `Course Lecturers`GROUP BY `Lecturer ID` HAVING `Lecturer ID` IN {lst} AND COUNT(`Lecturer ID`) < 6"
            cursor.execute(query)
            for lectID in cursor:
                lecturer = {}
                lecturer['Lecturer ID'] = lectID
                userLst.append(lecturer)
            conn.close()
            cursor.close()
        return make_response(userLst, 200) 
    except Exception as e:
        return make_response({"Failed": str(e)}, 400)

@app.route('/GreaterThan50', methods = ['GET'])
def greaterThan50():
    try:
        query = "SELECT * FROM `Greater Than 50 Students`"
        conn, cursor = connectToDB()
        cursor.execute(query)
        courseLst = []
        for studentCount, courseID, courseName in cursor:
            course = {}
            course['Student Count'] = studentCount
            course['Course ID'] = courseID
            course['Course Name'] = courseName
            courseLst.append(course)
        conn.close()
        cursor.close()
        return make_response(courseLst, 200)
    except Exception as e:
        return make_response({'Failed': str(e)}, 400)

@app.route('/Students5OrMore', methods = ['GET'])
def students5OrMore():
    try:
        query = "SELECT * FROM `Students Doing 5 or More Courses`"
        conn, cursor = connectToDB()
        cursor.execute(query)
        studentLst = []
        for courseCount, studentID, firstName, lastName in cursor:
            student = {}
            student['Course Count'] = courseCount
            student['Student ID'] = studentID
            student['First Name'] = firstName
            student['Last Name'] = lastName
            studentLst.append(student)
        conn.close()
        cursor.close()
        return make_response(studentLst, 200)
    except Exception as e:
        return make_response({'Failed': str(e)}, 400)

@app.route('/Lecturers3OrMore', methods = ['GET'])
def lecturers3OrMore():
    try:
        query = "SELECT * FROM `Lecturers Teaching 3 or More Courses`"
        conn, cursor = connectToDB()
        cursor.execute(query)
        lecturerLst = []
        for courseCount, lecturerID, firstName, lastName in cursor:
            lecturer = {}
            lecturer['Course Count'] = courseCount
            lecturer['Lecturer ID'] = lecturerID
            lecturer['First Name'] = firstName
            lecturer['Last Name'] = lastName
            lecturerLst.append(lecturer)
        conn.close()
        cursor.close()
        return make_response(lecturerLst, 200)
    except Exception as e:
        return make_response({'Failed': str(e)}, 400)

@app.route('/MostEnrolledCourses', methods = ['GET'])
def mostEnrolledCourses():
    try:
        query = "SELECT * FROM `10 Most Enrolled Courses`"
        conn, cursor = connectToDB()
        cursor.execute(query)
        courseLst = []
        for studentCount, courseID, courseName in cursor:
            course = {}
            course['Student Count'] = studentCount
            course['Course ID'] = courseID
            course['Course Name'] = courseName
            courseLst.append(course)
        conn.close()
        cursor.close()
        return make_response(courseLst, 200)
    except Exception as e:
        return make_response({'Failed': str(e)}, 400)

@app.route('/TopStudentAverages', methods = ['GET'])
def topStudentAverages():
    try:
        query = "SELECT * FROM `Top 10 Students By Average`"
        conn, cursor = connectToDB()
        cursor.execute(query)
        studentLst = []
        for studentAvg, studentID, firstName, lastName in cursor:
            student = {}
            student['Student Average'] = studentAvg
            student['Student ID'] = studentID
            student['First Name'] = firstName
            student['Last Name'] = lastName
            studentLst.append(student)
        conn.close()
        cursor.close()
        return make_response(studentLst, 200)
    except Exception as e:
        return make_response({'Failed': str(e)}, 400)

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
            print(eventLst)
        conn.close()
        cursor.close()
        return make_response(eventLst, 200)
    except Exception as e:
        return make_response({"Failed": str(e)}, 400)

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
        return make_response({"Failed": str(e)}, 400)

@app.route('/Availablecourses', methods = ['GET'])
def availCourses():
    try:
        query = "SELECT `Course ID`, `Course Name` FROM Courses WHERE `Course ID` NOT IN (SELECT `Course ID` FROM `Course Lecturers`);"
        conn, cursor = connectToDB()
        courseLst = []
        cursor.execute(query)
        for courseID, courseName in cursor:
            course = {}
            course['Course ID'] = courseID
            course['Course Name'] = courseName
            courseLst.append(course)
        print(courseLst)
        conn.close()
        cursor.close()
        return make_response(courseLst, 200)
    except Exception as e:
        return make_response({"Failed": str(e)}, 400)

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
        return make_response({"Failed": str(e)}, 400)

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
        return make_response({"Failed": str(e)}, 400)

@app.route('/StudentsByCourse/<course_id>', methods = ['GET'])
def studentsByCourse(course_id):
    try:
        query = f"SELECT Students.`Student ID`, Students.`First Name`, Students.`Last Name` FROM Students INNER JOIN `Course Students` ON Students.`Student ID` = `Course Students`.`Student ID` WHERE `Course Students`.`Course ID` = {course_id!r}"
        conn, cursor = connectToDB()
        cursor.execute(query)
        studentLst = []
        for studID, firstName, lastName in cursor:
            student = {}
            student['Student ID'] = studID
            student['First Name'] = firstName
            student['Last Name'] = lastName
            studentLst.append(student)
        conn.close()
        cursor.close()
        return make_response(studentLst, 200)
    except Exception as e:
        return make_response({"Failed": str(e)}, 400)

@app.route('/LecturerByCourse/<course_id>', methods = ['GET'])
def lecturerByCourse(course_id):
    try:
        query = f"SELECT Lecturers.`Lecturer ID`, Lecturers.`First Name`, Lecturers.`Last Name` FROM Lecturers INNER JOIN `Course Lecturers` ON Lecturers.`Lecturer ID` = `Course Lecturers`.`Lecturer ID` WHERE `Course Lecturers`.`Course ID` = {course_id!r}"
        lecturerLst = []
        conn, cursor = connectToDB()
        cursor.execute(query)
        row = cursor.fetchone()
        if row is not None:
            lectID, firstName, lastName = row
            lecturer = {}
            lecturer['Lecturer ID'] = lectID
            lecturer['First Name'] = firstName
            lecturer['Last Name'] = lastName
            lecturerLst.append(lecturer)
        conn.close()
        cursor.close()
        return make_response(lecturerLst, 200)
    except Exception as e:
        return make_response({"Failed": str(e)}, 400)

@app.route('/GetCourseMembers/<course_id>', methods = ['GET'])
def getCourseMembersByCourseID(course_id):
    return make_response(toList(lambda: studentsByCourse(course_id)) + toList(lambda: lecturerByCourse(course_id)), 200)

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
        return make_response({"Failed": str(e)}, 400)

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
            return make_response({"Failed": "User not found"}, 200)
    except Exception as e:
        return make_response({"Failed": str(e)}, 400)

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
        return make_response({"Failed": str(e)}, 400)

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
        return make_response({"Failed": str(e)}, 400)

# @app.route('/CreateCourse', methods = ['POST'])
# def createCourse():


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

@app.route(f'/{sN}/reports')
def reportsPage():
    return render_template("reports.html", reports = [{"Report Name":""}, {"Report Name":""}, {"Report Name":""}, {"Report Name":""}, {"Report Name":""}])

@app.route(f'/{sN}/addUser', methods = ['GET', 'POST'])
def addUserPage():
    form = AddUser()
    if form.validate_on_submit():
        try:
            conn, cursor = connectToDB()
            firstName = request.form['firstName'].capitalize()
            lastName = request.form['lastName'].capitalize()
            email = request.form['email']
            birthday = request.form['birthday']
            password = request.form['password']
            userChoice = request.form['userChoice']
            birthdaySplit = [int(birthday) for birthday in birthday.split("-")]
            age = date.today().year - birthdaySplit[0] - ((date.today().month, date.today().day) < (birthdaySplit[1], birthdaySplit[2]))
            if userChoice != "Admin":
                if userChoice == "Lecturer":
                    return redirect(url_for("selectCourse", firstName = firstName, lastName = lastName, email = email, age = age, birthday = birthday, password = password, userChoice = userChoice))
                else:
                    return redirect(url_for("selectCourse", firstName = firstName, lastName = lastName, email = email, age = age, birthday = birthday, password = password, userChoice = userChoice))
            else:
                try:
                    query = "SELECT COUNT(`Admin ID`) FROM Admins"
                    cursor.execute(query)
                    rowCount = cursor.fetchone()[0]               
                    query = f"INSERT INTO Admins VALUES('A{rowCount}', {firstName!r}, {lastName!r}, {email!r}, {age!r}, {birthday!r}, {password!r})"
                    cursor.execute(query)
                    conn.commit()
                    conn.close()
                    cursor.close()
                    return render_template("addUser.html", form = form, message = "User added succussfully")
                except Exception as e:
                    return make_response({"Failed": str(e)}, 400)
        except Exception as e:
            return make_response({"Failed": str(e)}, 400)
    return render_template("addUser.html", form = form)

@app.route(f'/{sN}/addCourse', methods = ['GET', 'POST'])
def addCoursePage():
    form = AddCourse()
    if form.validate_on_submit():
        try:
            studentIDs = list(set([studentID.strip() for studentID in request.form['studentIDs'].split(",")]))
            for studentID in studentIDs:
                if studentID[0] != "S" or studentID[1:].isdigit() == False:
                    invalidID = studentID
                    if len(studentIDs) < 10:
                        return render_template("addCourse.html", form = form, message = f"Invalid number of ID numbers, {10 - len(studentIDs)} more students needed")
                    return render_template("addCourse.html", form = form, message = f"{invalidID} is an invalid ID number")
            allStud = toList(lambda: availUsers("Student", studentIDs))
            notIn = []
            for stud in studentIDs:
                inside = False
                for studID in allStud:
                    if stud == studID['Student ID'][0]:
                        inside = True
                if inside == False:notIn.append(stud)
            if len(studentIDs) - len(notIn) < 10: return render_template("addCourse.html", form = form, message = f"{notIn} have reached the course threshold, class size less than 10, {10 - (len(studentIDs) - len(notIn))} more students needed")
            courseName = request.form['courseName'].title()
            courseLevel = request.form['courseLevel']
            query = "SELECT COUNT(`Course ID`) FROM courses"
            conn, cursor = connectToDB()
            cursor.execute(query)
            rowCount = cursor.fetchone()[0]
            courseID = courseLevel[0] + courseName[0] + str(rowCount)
            query = f"INSERT INTO Courses VALUES({courseID!r}, '{courseLevel}{courseName}')"
            conn.close()
            cursor.close()
            conn, cursor = connectToDB()
            cursor.execute(query)
            conn.commit()
            conn.close()
            cursor.close()

            conn, cursor = connectToDB()
            for stud in allStud:
                query = f"INSERT INTO `Course Students` VALUES({courseID!r}, {stud['Student ID'][0]!r}, {0!r})"
                cursor.execute(query)
                print(query)
            conn.commit()
            conn.close()
            cursor.close()
            if len(notIn) > 1 or len(studentIDs) - len(notIn) > 10: return render_template("addCourse.html", form = form, message = f"{notIn} have reached the course threshold, other students will be added")
        except Exception as e:
            return make_response({"Failed": str(e)}, 400)
    return render_template("addCourse.html", form = form)

@app.route(f'/{sN}/user/selectCourse/<firstName>&<lastName>&<email>&<age>&<birthday>&<password>&<userChoice>', methods = ['GET', 'POST'])
def selectCourse(firstName, lastName, email, age, birthday, password, userChoice):
    if request.method == "POST":
        try:
            
            selectedCourses = request.form.getlist('Selected Courses')
            print(selectedCourses, len(selectedCourses) < 3, userChoice == "Student", userChoice)
            if userChoice == "Student" and len(selectedCourses) < 3:
                return render_template("selectCourse.html", firstName = firstName, lastName = lastName, email = email, age = age, birthday = birthday, password = password, userChoice = userChoice, courses = toList(lambda: courses()), message = "Not enough courses are chosen")
            elif userChoice == "Lecturer" and len(selectedCourses) < 1:
                return render_template("selectCourse.html", firstName = firstName, lastName = lastName, email = email, age = age, birthday = birthday, password = password, userChoice = userChoice, courses = toList(lambda: availCourses()), message = "Not enough courses are chosen")

            userChoice += "s"
            query = f"SELECT COUNT(`{userChoice[:-1]} ID`) FROM {userChoice}"
            conn, cursor = connectToDB()
            cursor.execute(query)
           
            rowCount = cursor.fetchone()[0]
            userID = userChoice[0] + str(rowCount) 
            conn.close()
            cursor.close()

            query = f"INSERT INTO {userChoice} VALUES('{userChoice[0]}{rowCount}', {firstName!r}, {lastName!r}, {email!r}, {age!r}, {birthday!r}, {password!r})"
            conn, cursor = connectToDB()  
            cursor.execute(query)
            conn.commit()
            conn.close()
            cursor.close()

            conn, cursor = connectToDB()
            for course in selectedCourses:
                if userChoice == "Lecturers":
                    query = f"INSERT INTO `Course {userChoice}` VALUES({course!r}, {userID!r})"
                else:
                    query = f"INSERT INTO `Course {userChoice}` VALUES({course!r}, {userID!r}, '0')"
                cursor.execute(query)
            conn.commit()
            conn.close()
            cursor.close()
            return redirect(url_for('homePage'))
        except Exception as e:
            return make_response({"Failed": str(e)}, 400)
    if userChoice == "Student":
        return render_template("selectCourse.html", firstName = firstName, lastName = lastName, email = email, age = age, birthday = birthday, password = password, userChoice = userChoice, courses = toList(lambda: courses()))
    else:
         return render_template("selectCourse.html", firstName = firstName, lastName = lastName, email = email, age = age, birthday = birthday, password = password, userChoice = userChoice, courses = toList(lambda: availCourses()))       

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
            return make_response({"Failed": str(e)}, 400)  
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
            return make_response({"Failed": str(e)}, 400)
    return render_template("addAssignment.html", form = form, course_id = course_id)

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
    courseLecturer = toList(lambda: lecturerByCourse(course_id))
    courseStudents = toList(lambda: studentsByCourse(course_id))
    print(courseLecturer)
    return render_template("coursePage.html", course_id = course_id, course_name = course_name, calender = courseCalenders, assignments = courseAssignments, lecturer = courseLecturer, courseStudents = courseStudents)

if __name__ == 'main':
    app.run()