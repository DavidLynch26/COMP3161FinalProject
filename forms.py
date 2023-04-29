import email_validator
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, DataRequired, Email
from wtforms import StringField, PasswordField, DateField, validators, SelectMultipleField, SelectField

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class EventForm(FlaskForm):
    eventName = StringField('Event Name', validators=[InputRequired()])
    eventType = StringField('Event Type', validators=[InputRequired()])
    eventDescription = StringField('Username', validators=[InputRequired()])
    eventDate = DateField('Event Date', format = '%Y-%m-%d')

class AssignmentForm(FlaskForm):
    assignmentName = StringField('Assignment Name', validators=[InputRequired()])
    assignmentType = StringField('Assignment Type', validators=[InputRequired()])
    assignmentDescription = StringField('Assignment Description', validators=[InputRequired()])
    assignmentStartDate = DateField('Start Date', format = '%Y-%m-%d', validators=[InputRequired()])
    assignmentDueDate = DateField('Due Date', format = '%Y-%m-%d', validators=[InputRequired()])

class AddUser(FlaskForm):
    firstName = StringField('First Name', validators=[InputRequired()])
    lastName = StringField('Last Name', validators=[InputRequired()])
    email = StringField("Email",  [InputRequired("Please enter your email address."), Email("This field requires a valid email address")])
    birthday = DateField('Birthday', format = '%Y-%m-%d')
    password = PasswordField('Password', validators=[InputRequired()])
    userChoice = SelectField('User Type', choices = [("Admin", "Admin"), ("Student", "Student"), ("Lecturer", "Lecturer")])
    # categories = MultiCheckboxField('Courses',choices=[(course['Course ID'], course['Course Name']) for course in courses()])

class AddCourse(FlaskForm):
    courseName = StringField('Course Name', validators=[InputRequired()])    
    courseLevel = SelectField('Course Level', choices=[('Fundamentals in ', 'Fundamentals in '), ('Novice ', 'Novice '), ('Intermediate ', 'Intermediate '), ('Advanced ', 'Advanced '), ('Expert ', 'Expert ')])
    studentIDs = StringField('Student ID Numbers', validators=[InputRequired()])