# app/admin/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from .forms import CourseForm
from .. import db
from ..models import Course

def check_admin():
    '''
    Prevent non-admins from accessing the pags.
    '''

    if not current_user.is_admin:
        abort(403)

@admin.route('/courses', methods=['GET', 'POST'])
@login_required
def list_courses():
    '''
    List all courses.
    '''

    check_admin()

    courses = Course.query.all()

    return render_template('admin/courses/courses.html', courses=courses, title="Courses")

@admin.route('/courses/add', methods=['GET', 'POST'])
@login_required
def add_course():
    '''
    Add a course to the database
    '''

    check_admin()

    add_course = True

    form = CourseForm()
    if form.validate_on_submit():
        course = Course(
            course_name=form.name.data,
            credits=form.credits.data,
            teacher_id=form.teacher_id.data
        )

        try:
            # Add course to the database.
            db.session.add(course)
            db.session.commit()
            flash('You have successfully added a new course.')
        except:
            # In-cas course already exists.
            flash('Error: Course name already exists.')
    
        # Redirect to the course page.
        return redirect(url_for('admin.list_courses'))
    
    # Load course template.
    return render_template('admin/courses/course.html', action="Add", form=form, title="Add Course")    

@admin.route('/courses/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_course(id):
    '''
    Edit a course.
    '''

    check_admin()

    add_course = False

    course = Course.query.get_or_404(id)
    form = CourseForm(obj=course)
    if form.validate_on_submit():
        course.course_name = form.name.data
        course.credits = form.credits.data
        course.teacher_id = form.teacher_id.data
        
        db.session.commit()
        flash('You have successfully edited the course.')

        # REdirect to the courses page.
        return redirect(url_for('admin.list_courses'))

    form.name.data = course.course_name
    form.credits.data = course.credits
    form.teacher_id.data = course.teacher_id

    return render_template(
        'admin/courses/course.html', 
        action="Edit", 
        add_course=add_course, 
        form=form, 
        course=course, 
        title="Edit Course"
    )        

@admin.route('/courses/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_course(id):
    '''
    Delete a course from the database.
    '''

    check_admin()

    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    flash('You have successfully deleted the course.')

    # Redirect to the courses page.
    return redirect(url_for('admin.list_courses'))

    return render_template(title="Delete Course")
