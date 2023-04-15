import mysql.connector
from flask import Flask, request, make_response, render_template

app = Flask(__name__)

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

@app.route('/Courses', methods = ['GET']) #templte app.route
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
        query = "SELECT `Course Students`.`Course ID`, Courses.`Course Name` FROM `Course Students` RIGHT JOIN courses ON `Course Students`.`Course ID` = Courses.`Course ID` WHERE `Course Students`.`Student ID` = " + f"{student_id!r}"
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
        query = "SELECT `Course Lecturers`.`Course ID`, Courses.`Course Name` FROM `Course Lecturers` RIGHT JOIN courses ON `Course Lecturers`.`Course ID` = Courses.`Course ID` WHERE `Course Lecturers`.`Lecturer ID` = " + f"{lecturer_id!r}"
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

@app.route('/', methods = ['GET'])
def home():
    return render_template("home.html")

if __name__ == 'main':
    app.run()