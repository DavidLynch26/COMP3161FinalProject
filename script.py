import csv
import names
import string
import pandas as pd
import random2 as random
from datetime import date

header = ['ID Number', 'First Name', 'Last Name', 'Email', 'Age', 'Birthday', 'Password']

def generateStudent(id):
    end_date = date.today()
    end_date = end_date.replace(year = end_date.year - 18)
    start_date = end_date.replace(year=end_date.year - 11)
    birthday = date.fromordinal(random.randint(start_date.toordinal(), end_date.toordinal()))
    age = date.today().year - birthday.year - ((date.today().month, date.today().day) < (birthday.month, birthday.day))
    birthday = f"{birthday:%b %d %Y}"

    fullName = names.get_full_name()
    firstName, lastName = fullName.split(' ')
    password = ''.join([random.choice(string.ascii_letters + string.digits + string.punctuation) for n in range(random.randint(8, 16))])

    return {'ID Number': id, 
    'First Name': firstName,
    'Last Name': lastName,
    'Email': firstName+"."+lastName+"@mymona.uwi.edu", 
    'Age': age,
    'Birthday': birthday, 
    'Password': password}

try:
    with open('students.csv', 'w+', encoding = 'UTF8', newline = '') as f:
        writer = csv.writer(f, )
        writer.writerow(header)
        for n in range(10):
            student = generateStudent(n)
            writer.writerow([student['ID Number'], student['First Name'], student['Last Name'], student['Email'], student['Age'], student['Birthday'], student['Password']])
        f.close()
except Exception as e:
    print(str(e))