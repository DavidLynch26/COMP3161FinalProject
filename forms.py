from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, validators, SelectMultipleField
from wtforms.validators import InputRequired
from wtforms.validators import DataRequired
from email import message

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class EventForm(FlaskForm):
    eventName = StringField('Event Name', validators=[InputRequired()])
    eventType = StringField('Event Type', validators=[InputRequired()])
    eventDescription = StringField('Username', validators=[InputRequired()])
    eventDate = DateField('Event Date', format = '%d/%m/%Y', validators=[InputRequired()])

class AssignmentForm(FlaskForm):
    assignmentName = StringField('Assignment Name', validators=[InputRequired()])
    assignmentType = StringField('Assignment Type', validators=[InputRequired()])
    assignmentDescription = StringField('Assignment Description', validators=[InputRequired()])
    assignmentStartDate = DateField('Start Date', format = '%d/%m/%Y', validators=[InputRequired()])
    assignmentDueDate = DateField('Due Date', format = '%d/%m/%Y', validators=[InputRequired()])

class AddUser(FlaskForm):
    firstName = StringField('First Name', validators=[InputRequired()])
    lastNamee = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', [ validators.DataRequired(), validators.Email("Please enter a valid email")])
    birthday = StringField('Birthday', validators=[InputRequired()])
    password = StringField('Password', validators=[InputRequired()])
    # categories = MultiCheckboxField('Categories',choices=[('news', 'News'), ('tutorial', 'Tutorial'), ('reviews', 'Reviews'), ('recommendations', 'Recommendations')
