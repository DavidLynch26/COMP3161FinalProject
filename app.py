import os
import mysql.connector
from forms import LoginForm
from flask import Flask, request, make_response, render_template

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

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
def Courses():
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
        print(str(e))

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
        print(str(e))

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

# @app.route('/Login/<user_id>&<user_password>', methods = ['POST'])
# def login(user_id, user_password):
#     try:
#         if(user_id[0] == "S"):
#             query = f"SELECT * FROM Students WHERE `Student ID` = {user_id!r} AND Password = {user_password!r}"
#         else:
#             query = f"SELECT * FROM Lecturers WHERE `Lecturer ID` = {user_id!r} AND Password = {user_password!r}"
#         conn, cursor = connectToDB()
#         loginStatus = ""
#         cursor.execute(query)
#         row = cursor.fetchone()
#         if row is not None:
#             if(user_id[0] == "S"):
#                 studentID, firstName, lastName, email, age, birthday, password = row
#                 student = {}
#                 student['Student ID'] = studentID
#                 student['First Name'] = firstName
#                 student['Last Name'] = lastName
#                 student['Email'] = email
#                 student['Age'] = age
#                 student['Birthday'] = birthday
#                 student['Password'] = password
#                 loginStatus = "Student login successful"
#             else:
#                 lecturerID, firstName, lastName, email, age, birthday, password = row
#                 lecturer = {}
#                 lecturer['Lecturer ID'] = lecturerID
#                 lecturer['First Name'] = firstName
#                 lecturer['Last Name'] = lastName
#                 lecturer['Email'] = email
#                 lecturer['Age'] = age
#                 lecturer['Birthday'] = birthday
#                 lecturer['Password'] = password
#                 loginStatus = "Lecturer login successful"
#             return make_response(loginStatus, 200)
#         else:
#             return make_response("User not found", 200)
#     except Exception as e:
#         return make_response(str(e), 400)

@app.route('/login', methods = ['GET'])
def login():
    form = LoginForm()
    # if form.validate_on_submit():
    #     return "asd"
    return render_template("login.html", form = form)

if __name__ == 'main':
    app.run()