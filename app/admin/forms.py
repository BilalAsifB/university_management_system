# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField   
from wtforms.validators import DataRequired, ValidationError
from ..models import Teacher, Department

class CourseForm(FlaskForm):
    '''
    Form for admin to add or edit a Course.
    '''

    name = StringField('Name', validators=[DataRequired()])
    credits = IntegerField('Credits', validators=[DataRequired()])
    teacher_id = IntegerField('Teacher ID', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_teacher_id(self, field):
        '''
        Check if the teacher_id exists in the Teacher table.
        '''

        teacher = Teacher.query.get(field.data)
        if not teacher:
            raise ValidationError('Invalid Teacher ID!')

class StudentForm(FlaskForm):
    '''
    Form for admin to edit a student.
    '''

    department_id = IntegerField('Department ID', validators=[DataRequired()])

    def validate_department_id(self, field):
        '''
        Check if the department_id exists in the Department table.
        '''

        department = Department.query.get(field.data)
        if not department:
            raise ValidationError('Invalid Department ID!')
        
class TeacherForm(FlaskForm):
    '''
    Form for admin to edit a teacher.
    '''

    speciality_choices = ['CS', 'NS', 'AI', 'EE', 'MG', 'MT']

    speciality = SelectField(
        'Speciality', 
        choices=[('CS', 'CS'), ('NS', 'NS'), ('AI', 'AI'), ('EE', 'EE'), ('MG', 'MG'), ('MT', 'MT')],
        validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_specialifty(self, field):
        if field.data not in self.speciality_choices:
            raise ValidationError('Invalid speciality!')
        
class VerifyUserForm(FlaskForm):
    '''
    Form for admin to verify a user.
    '''
    
    submit = SubmitField('Verify User')
        