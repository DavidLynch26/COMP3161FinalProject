import csv
import names
import string
import pandas as pd
import mysql.connector
import random2 as random
from datetime import date

def connectToDB():
    conn = mysql.connector.connect(
        user = username,
        password = password,
        host = host,  
        database = database
     )
    cursor = conn.cursor()

    return conn, cursor

def generateUser(type, id):

    end_date = date.today()

    if type == "S":
        end_date = end_date.replace(year = end_date.year - 18)
        emailType = "@mymona.uwi.edu"
    else:
        end_date = end_date.replace(year = end_date.year - 30)
        emailType = "@uwimona.edu.jm"
    
    start_date = end_date.replace(year=end_date.year - 11)
    birthday = date.fromordinal(random.randint(start_date.toordinal(), end_date.toordinal()))
    age = date.today().year - birthday.year - ((date.today().month, date.today().day) < (birthday.month, birthday.day))
    birthday = f"{birthday:%Y-%m-%d}"

    fullName = names.get_full_name()
    firstName, lastName = fullName.split(' ')
    password = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(random.randint(8, 16))])

    id = type + str(id)

    return {'ID Number': id,
    'First Name': firstName,
    'Last Name': lastName,
    'Email': firstName+"."+lastName+emailType,
    'Age': age,
    'Birthday': birthday,
    'Password': password}

host = "localhost"
username = "DavidLynch"
password = "tJ58FIU!uuV/3HS8"
database = "comp3161_final_project"

tableNames = ["Courses", 
            "Students", 
            "Lecturers",
            "Course Students",
            "Course Lecturers"]
            
database = "comp3161_final_project"

header = [["Course ID", "Course Name"], 
        ["Student ID", "First Name", "Last Name", "Email", "Age", "Birthday", "Password"], 
        ["Lecturer ID", "First Name", "Last Name", "Email", "Age", "Birthday", "Password"],
        ["Student ID", "Course ID", "Grade"],
        ["Lecturer ID", "Course ID"]]

levels = ["Fundamentals in ", "Novice ", "Intermediate ", "Advanced ", "Expert "]
courseSubjects = ["Python", "Javascript", "C#", "Java", "C", "C++", "PHP", "Kotlin", "R", "HTML", "CSS", "Swift", "GO", "Ruby", "Pascal", "Dart", "Pascal", "Rust", "Cobol", "Calculus", "Calculus", "Electronic Circuit Analysis", "Statistics", "Chemistry", "Biology", "Physics", "Information Technology", "Calculus 2", "Electronics", "Physical Education", "Health and Nutrition", "Home and Family Life Education", "Civics", "Carpentry", "Welding", "Telecommunications", "Machinery", "Web DEvelopement", "Database Management", "Discrete Mathematics"]
courses = [[x[0] + y[0:1] + str(n), x+y] for x in levels for n, y in enumerate(courseSubjects)]
lecturers = []
courseStudents = []
courseLecturers = []

for n in range(1, 6):
    for y in range(2):
        for x in range(5):
            lecturers.append(generateUser("L", len(lecturers)))
            courseLecturers.append([["CourseID"]*n, lecturers[-1]["ID Number"]])
for n in range(10):
    lecturers.append(generateUser("L", len(lecturers)))
    courseLecturers.append([["CourseID"]*5, lecturers[-1]["ID Number"]])

counter = 0

# count = 0
# for n in courseLecturers:
#     count += n[1].count("CourseID")
# print(count)



# def factorize(a, b, n):
#     return n/a, (n%a)/b, (n%a)%b

# def factorize_min(a, b, n):
#     na1, nb1, r1 = factorize(a, b, n)
#     nb2, na2, r2 = factorize(b, a, n)
#     return (na1, nb1) if r1 < r2 else (na2, nb2)

# def factorize_min_list(a, b, n):
#     na, nb = factorize_min(a, b, n)
#     na = int(na)
#     nb = int(nb)
#     return [a]*na + [b]*nb

try:
    f = open("script.sql", "w+")
    f.writelines([f"DROP DATABASE IF EXISTS {database};\n", 
    f"CREATE DATABASE {database};\n",
    f"USE {database};\n\n"])

    f.writelines([f"DROP TABLE IF EXISTS {tableNames[0]};\n",
        f"CREATE TABLE {tableNames[0]}(\n",
        f"  `{header[0][0]}` VARCHAR(255) NOT NULL PRIMARY KEY,\n",
        f"  `{header[0][1]}` VARCHAR(255)\n"
        ");\n\n"])

    f.writelines([f"DROP TABLE IF EXISTS {tableNames[1]};\n",
        f"CREATE TABLE {tableNames[1]}(\n",
        f"  `{header[1][0]}` VARCHAR(255) NOT NULL PRIMARY KEY,\n",
        f"  `{header[1][1]}` VARCHAR(255),\n",
        f"  `{header[1][2]}` VARCHAR(255),\n",
        f"  {header[1][3]} VARCHAR(255),\n",
        f"  {header[1][4]} INTEGER,\n",
        f"  {header[1][5]} DATE,\n",
        f"  {header[1][6]} VARCHAR(255)\n"
        ");\n\n"])
    
    f.writelines([f"DROP TABLE IF EXISTS {tableNames[2]};\n",
        f"CREATE TABLE {tableNames[2]}(\n",
        f"  `{header[2][0]}` VARCHAR(255) NOT NULL PRIMARY KEY,\n",
        f"  `{header[2][1]}` VARCHAR(255),\n",
        f"  `{header[2][2]}` VARCHAR(255),\n",
        f"  {header[2][3]} VARCHAR(255),\n",
        f"  {header[2][4]} INTEGER,\n",
        f"  {header[2][5]} DATE,\n",
        f"  {header[2][6]} VARCHAR(255)\n"
        ");\n\n"])

    f.writelines([f"DROP TABLE IF EXISTS `{tableNames[3]}`;\n",
        f"CREATE TABLE `{tableNames[3]}`(\n",
        f"  `{header[3][0]}` VARCHAR(255),\n",
        f"  `{header[3][1]}` VARCHAR(255),\n",
        f"  {header[3][2]} INTEGER\n"
        ");\n\n"])
    
    f.writelines([f"DROP TABLE IF EXISTS `{tableNames[4]}`;\n",
        f"CREATE TABLE `{tableNames[4]}`(\n",
        f"  `{header[4][0]}` VARCHAR(255),\n",
        f"  `{header[4][1]}` VARCHAR(255)\n"
        ");\n\n"])    

    with open('courses.csv', 'w+', encoding = 'UTF8', newline = '') as c, open('students.csv', 'w+', encoding = 'UTF8', newline = '') as s, open('lecturers.csv', 'w+', encoding = 'UTF8', newline = '') as l, open('Courses_Students.csv', 'w+', encoding = 'UTF8', newline = '') as cs, open('Courses_Lecturer.csv', 'w+', encoding = 'UTF8', newline = '') as cl:
        writer = csv.writer(c)
        writer.writerow(header[0])
        for course in courses:
            writer.writerow(course)
            f.writelines([f"INSERT INTO {tableNames[0]} ",
            f"VALUES({course[0]!r}, {course[1]!r});\n"])
        f.write("\n")

        writer = csv.writer(s)
        writer.writerow(header[1])
        for n in range(100): #Change to appropriate value
            student = generateUser("S", n)
            writer.writerow([student['ID Number'], student['First Name'], student['Last Name'], student['Email'], student['Age'], student['Birthday'], student['Password']])
                    
            f.writelines([f"INSERT INTO {tableNames[1]} ",
            f"VALUES({student['ID Number']!r}, {student['First Name']!r}, {student['Last Name']!r}, {student['Email']!r}, {student['Age']!r}, {student['Birthday']!r}, {student['Password']!r});\n"])
        f.write("\n")

        writer = csv.writer(l)
        writer.writerow(header[2])
        for lecturer in lecturers:
            writer.writerow([lecturer['ID Number'], lecturer['First Name'], lecturer['Last Name'], lecturer['Email'], lecturer['Age'], lecturer['Birthday'], lecturer['Password']])

            f.writelines([f"INSERT INTO {tableNames[2]} ",
            f"VALUES({lecturer['ID Number']!r}, {lecturer['First Name']!r}, {lecturer['Last Name']!r}, {lecturer['Email']!r}, {lecturer['Age']!r}, {lecturer['Birthday']!r}, {lecturer['Password']!r});\n"])
        f.write("\n")            

        writer = csv.writer(cs)
        writer.writerow(header[3])
        for courseStudent in courseStudents:
            for courseGrade in courseStudent[1]:
                f.writelines([f"INSERT INTO `{tableNames[3]}` ",
                f"VALUES({courseStudent[0]!r}, {courseGrade[0]!r}, {courseGrade[1]!r});\n"])
                writer.writerow([courseStudent[0], courseGrade[0], courseGrade[1]])

        writer = csv.writer(cl)
        writer.writerow(header[4])
        for courseLecturer in courseLecturers:
            for course in courseLecturer[0]:
                f.writelines([f"INSERT INTO `{tableNames[4]}` ",
                f"VALUES({courseLecturer[1]!r}, {courses[counter][0]!r});\n"])
                writer.writerow([courseLecturer[1], courses[counter][0]])
                counter += 1
    f.close()
except Exception as e:
    print(str(e))