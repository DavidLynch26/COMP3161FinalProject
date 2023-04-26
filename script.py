import csv
import names
import string
import pandas as pd
import mysql.connector
import random2 as random
from datetime import date

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

tableNames = ["courses", 
            "admins",
            "students", 
            "lecturers",
            "course students",
            "course lecturers",
            "course assignments",
            "course calenders"]
            
database = "comp3161_final_project"

header = [["Course ID", "Course Name"], 
        ["Admin ID", "First Name", "Last Name", "Email", "Age", "Birthday", "Password"],
        ["Student ID", "First Name", "Last Name", "Email", "Age", "Birthday", "Password"], 
        ["Lecturer ID", "First Name", "Last Name", "Email", "Age", "Birthday", "Password"],
        ["Course ID", "Student ID", "Grade"],
        ["Lecturer ID", "Course ID"],
        ["Assignment ID", "Name", "Type", "Description", "Course ID"],
        ["Calender ID", "Name", "Type", "Description", "Course ID"]]

levels = ["Fundamentals in ", "Novice ", "Intermediate ", "Advanced ", "Expert "]
courseSubjects = ["Python", "Javascript", "C#", "Java", "C", "C++", "PHP", "Kotlin", "R", "HTML", "CSS", "Swift", "GO", "Ruby", "Pascal", "Dart", "Pascal", "Rust", "Cobol", "Calculus", "Calculus", "Electronic Circuit Analysis", "Statistics", "Chemistry", "Biology", "Physics", "Information Technology", "Calculus 2", "Electronics", "Physical Education", "Health and Nutrition", "Home and Family Life Education", "Civics", "Carpentry", "Welding", "Telecommunications", "Machinery", "Web Developement", "Database Management", "Discrete Mathematics"]

courses = [[x[0] + y[0:1] + str(n), x+y] for x in levels for n, y in enumerate(courseSubjects)]
admins = []
lecturers = []
courseStudents = [] 
courseLecturers = []

for count, course in enumerate(courses):
    tempLst = []
    for studCount in range(count*10, count*10+10):
        tempLst += ["S" + str(studCount)]
    courseStudents.append([course[0], tempLst])

for n in range(1, 6):
    for y in range(2):
        for x in range(5):
            lecturers.append(generateUser("L", len(lecturers)))
            courseLecturers.append([["CourseID"]*n, lecturers[-1]["ID Number"]])
for n in range(10):
    lecturers.append(generateUser("L", len(lecturers)))

    admins.append(generateUser("A", len(admins)))
    admins.append(generateUser("A", len(admins)))

    courseLecturers.append([["CourseID"]*5, lecturers[-1]["ID Number"]])    

def createStudentsFile(f):
    f.writelines([f"DROP TABLE IF EXISTS {tableNames[2]};\n",
    f"CREATE TABLE {tableNames[2]}(\n",
    f"  `{header[2][0]}` VARCHAR(255) NOT NULL PRIMARY KEY,\n",
    f"  `{header[2][1]}` VARCHAR(255),\n",
    f"  `{header[2][2]}` VARCHAR(255),\n",
    f"  {header[2][3]} VARCHAR(255),\n",
    f"  {header[2][4]} INTEGER,\n",
    f"  {header[2][5]} DATE,\n",
    f"  {header[2][6]} VARCHAR(255)\n"
    ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;\n\n"])

    with open('students.csv', 'w+', encoding = 'UTF8', newline = '') as s:
        writer = csv.writer(s)
        writer.writerow(header[2])
        f.write("LOCK TABLES `students` WRITE;\n")
        for n in range(100000): #Change to appropriate value
            student = generateUser("S", n)
            writer.writerow([student['ID Number'], student['First Name'], student['Last Name'], student['Email'], student['Age'], student['Birthday'], student['Password']])

            if n > 1999:
                randNum = random.randint(3,6)
                for x in range(randNum):
                    randCourse = random.randint(0,199)
                    while student['ID Number'] in courseStudents[randCourse][1]:
                        randCourse = random.randint(0,199)
                    courseStudents[randCourse][1] += [student['ID Number']]
            else:
                randNum = random.randint(3,5)
                for x in range(randNum):
                    randCourse = random.randint(0,199)
                    while student['ID Number'] in courseStudents[randCourse][1]:
                        randCourse = random.randint(0,199)
                    courseStudents[randCourse][1] += [student['ID Number']]

            f.writelines([f"INSERT INTO {tableNames[2]} ",
            f"VALUES({student['ID Number']!r}, {student['First Name']!r}, {student['Last Name']!r}, {student['Email']!r}, {student['Age']!r}, {student['Birthday']!r}, {student['Password']!r});\n"])
        f.write("UNLOCK TABLES;\n\n")

def createCoursesFile(f):
    f.writelines([f"DROP TABLE IF EXISTS {tableNames[0]};\n",
        f"CREATE TABLE {tableNames[0]}(\n",
        f"  `{header[0][0]}` VARCHAR(255) NOT NULL PRIMARY KEY,\n",
        f"  `{header[0][1]}` VARCHAR(255)\n"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;\n\n"])

    with open('courses.csv', 'w+', encoding = 'UTF8', newline = '') as c:
        writer = csv.writer(c)
        writer.writerow(header[0])
        f.write("LOCK TABLES `courses` WRITE;\n")
        for course in courses:
            writer.writerow(course)
            f.writelines([f"INSERT INTO {tableNames[0]} ",
            f"VALUES({course[0]!r}, {course[1]!r});\n"])
        f.write("UNLOCK TABLES;\n\n")

def createAdminsFile(f):
    f.writelines([f"DROP TABLE IF EXISTS {tableNames[1]};\n",
        f"CREATE TABLE {tableNames[1]}(\n",
        f"  `{header[1][0]}` VARCHAR(255) NOT NULL PRIMARY KEY,\n",
        f"  `{header[1][1]}` VARCHAR(255),\n",
        f"  `{header[1][2]}` VARCHAR(255),\n",
        f"  {header[1][3]} VARCHAR(255),\n",
        f"  {header[1][4]} INTEGER,\n",
        f"  {header[1][5]} DATE,\n",
        f"  {header[1][6]} VARCHAR(255)\n"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;\n\n"])

    with open('admins.csv', 'w+', encoding = 'UTF8', newline = '') as a:
        writer = csv.writer(a)
        writer.writerow(header[1])
        f.write("LOCK TABLES `admins` WRITE;\n")
        for admin in admins:
            writer.writerow([admin['ID Number'], admin['First Name'], admin['Last Name'], admin['Email'], admin['Age'], admin['Birthday'], admin['Password']])

            f.writelines([f"INSERT INTO {tableNames[1]} ",
            f"VALUES({admin['ID Number']!r}, {admin['First Name']!r}, {admin['Last Name']!r}, {admin['Email']!r}, {admin['Age']!r}, {admin['Birthday']!r}, {admin['Password']!r});\n"])
        f.write("UNLOCK TABLES;\n\n")

def createCourseStudentsFile(f):
    f.writelines([f"DROP TABLE IF EXISTS `{tableNames[4]}`;\n",
        f"CREATE TABLE `{tableNames[4]}`(\n",
        f"  `{header[4][0]}` VARCHAR(255),\n",
        f"  `{header[4][1]}` VARCHAR(255),\n",
        f"  {header[4][2]} INTEGER\n"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;\n\n"])

    with open('Courses_Students.csv', 'w+', encoding = 'UTF8', newline = '') as cs:
        writer = csv.writer(cs)
        writer.writerow(header[4])
        f.write("LOCK TABLES `course students` WRITE;\n")
        for courseStudent in courseStudents:
            for courseStud in courseStudent[1]:
                randGrade = random.randint(0,100)
                f.writelines([f"INSERT INTO `{tableNames[4]}` ",
                f"VALUES({courseStudent[0]!r}, {courseStud!r}, {randGrade!r});\n"])
                writer.writerow([courseStudent[0], courseStud, randGrade])
        f.write("UNLOCK TABLES;\n\n")

def createCourseLecturersFile(f):
    f.writelines([f"DROP TABLE IF EXISTS `{tableNames[5]}`;\n",
        f"CREATE TABLE `{tableNames[5]}`(\n",
        f"  `{header[5][0]}` VARCHAR(255),\n",
        f"  `{header[5][1]}` VARCHAR(255)\n"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;\n\n"])    

    with open('Courses_Lecturer.csv', 'w+', encoding = 'UTF8', newline = '') as cl:
        writer = csv.writer(cl)
        writer.writerow(header[5])
        counter = 0
        f.write("LOCK TABLES `course lecturers` WRITE;\n")
        for courseLecturer in courseLecturers:
            for course in courseLecturer[0]:
                f.writelines([f"INSERT INTO `{tableNames[5]}` ",
                f"VALUES({courseLecturer[1]!r}, {courses[counter][0]!r});\n"])
                writer.writerow([courseLecturer[1], courses[counter][0]])
                counter += 1    
        f.write("UNLOCK TABLES;\n\n")

def createLecturersFile(f):
    f.writelines([f"DROP TABLE IF EXISTS {tableNames[3]};\n",
        f"CREATE TABLE {tableNames[3]}(\n",
        f"  `{header[3][0]}` VARCHAR(255) NOT NULL PRIMARY KEY,\n",
        f"  `{header[3][1]}` VARCHAR(255),\n",
        f"  `{header[3][2]}` VARCHAR(255),\n",
        f"  {header[3][3]} VARCHAR(255),\n",
        f"  {header[3][4]} INTEGER,\n",
        f"  {header[3][5]} DATE,\n",
        f"  {header[3][6]} VARCHAR(255)\n"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;\n\n"]) 

    with open('lecturers.csv', 'w+', encoding = 'UTF8', newline = '') as l:
        writer = csv.writer(l)
        writer.writerow(header[3])
        for lecturer in lecturers:
            writer.writerow([lecturer['ID Number'], lecturer['First Name'], lecturer['Last Name'], lecturer['Email'], lecturer['Age'], lecturer['Birthday'], lecturer['Password']])

            f.writelines([f"INSERT INTO {tableNames[3]} ",
            f"VALUES({lecturer['ID Number']!r}, {lecturer['First Name']!r}, {lecturer['Last Name']!r}, {lecturer['Email']!r}, {lecturer['Age']!r}, {lecturer['Birthday']!r}, {lecturer['Password']!r});\n"])
        f.write("\n\n")      

def createCourseAssignments(f):
    f.writelines([f"DROP TABLE IF EXISTS `{tableNames[6]}`;\n",
        f"CREATE TABLE `{tableNames[6]}`(\n",
        f"  `{header[6][0]}` VARCHAR(255) NOT NULL PRIMARY KEY,\n",
        f"  {header[6][1]} VARCHAR(255),\n",
        f"  {header[6][2]} VARCHAR(255),\n",
        f"  {header[6][3]} VARCHAR(255),\n",
        f"  `{header[6][4]}` VARCHAR(255)\n"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;\n\n"])     

def createCourseCalenders(f):
    f.writelines([f"DROP TABLE IF EXISTS `{tableNames[7]}`;\n",
        f"CREATE TABLE `{tableNames[7]}`(\n",
        f"  `{header[7][0]}` VARCHAR(255) NOT NULL PRIMARY KEY,\n",
        f"  {header[7][1]} VARCHAR(255),\n",
        f"  {header[7][2]} VARCHAR(255),\n",
        f"  {header[7][3]} VARCHAR(255),\n",
        f"  `{header[7][4]}` VARCHAR(255)\n"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;\n\n"])   

functionDict = {
    'cc': createCourseCalenders,
    'ca': createCourseAssignments,
    'a': createAdminsFile,
    's': createStudentsFile,
    'c': createCoursesFile,
    'l': createLecturersFile,
    'cl': createCourseLecturersFile,
    'cs': createCourseStudentsFile}

def createFiles(lst):
    if lst == ["All"]:
        f = open("script.sql", "w+")
        f.writelines([f"DROP DATABASE IF EXISTS {database};\n", 
        f"CREATE DATABASE {database};\n",
        f"USE {database};\n\n"])  
        for key, val in functionDict.items():
            val(f)
    else:
        f = open("script.sql", "a")
        for func in lst:
            if func in functionDict:
                functionDict[func](f)     
    f.close()

try:
    createFiles(["ca", "cc"])
except Exception as e:
    logger.exception(str(e))