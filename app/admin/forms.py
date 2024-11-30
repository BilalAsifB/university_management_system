# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField   
from wtforms.validators import DataRequired, ValidationError
from ..models import Teacher

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
      
