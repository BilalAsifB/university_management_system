# app/auth/forms.py

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length 

from ..models import User

class RegistrationForm(FlaskForm):
    '''
    Form for users to create new account.
    '''

    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    contact = StringField('Contact', validators=[DataRequired(), Length(min=10, max=15)])
    address = StringField('Address', validators=[DataRequired(), Length(max=200)])
    role = SelectField(
        'Role',
        choices=[('Student', 'Student'), ('Teacher', 'Teacher'), ('Admin', 'Admin')],
        validators=[DataRequired()]
    )
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use!')
    
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use!')
        
    def validate_contact(self, field):
        if User.query.filter_by(contact=field.data).first():
            raise ValidationError('Contact number is already in use!')
        
    def validate_role(self, field):
        if field.data not in ['Student', 'Teacher', 'Admin']:
            raise ValidationError('Invalid role selected!')
        
class LoginForm(FlaskForm):
    '''
    Form for users to login.
    '''

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    