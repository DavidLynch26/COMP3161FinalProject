import script
import mysql.connector
from flask import Flask, request, make_response

app = Flask(__name__)

@app.route('/Courses', methods = ['GET']) #templte app.route
def Courses():
    try:
        query = "SELECT * FROM Courses"
        conn, cursor = script.connectToDB()
        courseLst = []
        cursor.execute(query)
        for idNumber, courseName, courseCapacity in cursor:
            course = {}
            course['Course ID'] = idNumber
            course['Course Name'] = courseName
            course['Course Capacity'] = courseCapacity
            courseLst.append(course)
        conn.close()
        cursor.close()
        return make_response(courseLst, 200)
    except Exception as e:
        print(str(e))

@app.route('/Courses/<student_id>', methods = ['GET'])
def courseByStudent(student_id):
    try:
        query = "SELECT `Course ID`, `Course Name`, `Course Capacity` FROM studentcourse WHERE `Student ID` = " + student_id
        conn, cursor = script.connectToDB()
        courseLst = []
        cursor.execure(query)
        for courseID, courseName, courseCapacity in cursor:
            course = {}
            course['Course ID'] = courseID
            course['Course Name'] = courseName
            course['Course Capacity'] = courseCapacity
            courseLst.append(course)
        conn.close()
        cursor.close()
        return make_response(courseLst, 200)
    except Exception as e:
        print(str(e))

@app.route('/Courses/<lecturer_id>', methods = ['GET'])
def courseByLecturer(lecturer_id):
    try:
        query = "SELECT `Course ID`, `Course Name`, `Course Capacity` FROM lecturercourse WHERE `Lecturer ID` = " + lecturer_id
        conn, cursor = script.connectToDB()
        courseLst = []
        cursor.execure(query)
        for courseID, courseName, courseCapacity in cursor:
            course = {}
            course['Course ID'] = courseID
            course['Course Name'] = courseName
            course['Course Capacity'] = courseCapacity
            courseLst.append(course)
        conn.close()
        cursor.close()
        return make_response(courseLst, 200)
    except Exception as e:
        print(str(e))

# @app.route('/Members/<course_id>', methods = ['GET'])
# def membersByCourse(course_id):
#     try:
#         query = "SELECT ``"
#     except Exception as e:
#         print(str(e))

if __name__ == 'main':
    app.run()