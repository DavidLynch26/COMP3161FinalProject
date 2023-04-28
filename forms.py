from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField
from wtforms.validators import InputRequired

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

# class AddUser(FlaskForm):
