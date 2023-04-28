import email_validator
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, DataRequired
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
    email = StringField('Email', [ validators.DataRequired(), validators.Email("Please enter a valid email")])
    birthday = StringField('Birthday', validators=[InputRequired()])
    password = StringField('Password', validators=[InputRequired()])
    # categories = MultiCheckboxField('Categories',choices=[('news', 'News'), ('tutorial', 'Tutorial'), ('reviews', 'Reviews'), ('recommendations', 'Recommendations')

class AddCourse(FlaskForm):
    courseName = StringField('Course Name', validators=[InputRequired()])    
     #categories = MultiCheckboxField('Categories',choices=[('news', 'News'), ('tutorial', 'Tutorial'), ('reviews', 'Reviews'), ('recommendations', 'Recommendations')
     #categories = MultiCheckboxField('Categories',choices=[('news', 'News'), ('tutorial', 'Tutorial'), ('reviews', 'Reviews'), ('recommendations', 'Recommendations')
     #categories = SelectField('Categories', choices=[('house', 'House'), ('apartment', 'Apartment')])