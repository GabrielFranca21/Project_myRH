from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email

class EmployeeForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    department = StringField('Department', validators=[DataRequired()])
    hiring_date = DateField('Hiring Date', format='%Y-%m-%d', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    address = StringField('Address')
    skills = TextAreaField('Skills')
    submit = SubmitField('Submit')
