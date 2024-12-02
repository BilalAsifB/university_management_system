# app/admin/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from .forms import CourseForm, StudentForm, TeacherForm,VerifyUserForm
from .. import db
from ..models import Course, Student, Teacher, User

def check_admin():
    '''
    Prevent non-admins from accessing the pags.
    '''

    if not current_user.is_admin:
        abort(403)

# Course Views.

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

# Student Views.

@admin.route('/students', methods=['GET', 'POST'])
@login_required
def list_students():
    '''
    List all students.
    '''

    check_admin()

    students = Student.query.all()

    return render_template('admin/students/students.html', students=students, title="Students")

@admin.route('/students/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_student(id):
    '''
    Edit a student.
    '''

    check_admin()

    student = Student.query.get_or_404(id)
    form = StudentForm(obj=student)
    if form.validate_on_submit():
        student.department_id = form.department_id.data
        db.session.commit()
        flash('You have successfully edited the student.')

        # Reirect to the students page.
        return redirect(url_for('admin.list_students'))
    
    form.department_id.data = student.department_id
    return render_template(
        'admin/students/student.html', 
        action="Edit",
        form=form,
        student=student,
        title="Edit Student"
    )

@admin.route('/students/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_student(id):
    '''
    Delete a student from the database.
    '''

    check_admin()

    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash('You have successfully deleted the student.')

    # Redirect to the students page.
    return redirect(url_for('admin.list_students'))

    return render_template(title="Delete Student")


# Teacher Views.

@admin.route('/teachers', methods=['GET', 'POST'])
@login_required
def list_teachers():
    '''
    List all teachers.
    '''

    check_admin()

    teachers = Teacher.query.all()

    return render_template('admin/teachers/teachers.html', teachers=teachers, title="Teachers")

@admin.route('/teachers/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_teacher(id):
    '''
    Edit a teacher.
    '''

    check_admin()

    teacher = Teacher.query.get_or_404(id)
    form = TeacherForm(obj=teacher)
    if form.validate_on_submit():
        teacher.speciality = form.speciality.data
        db.session.commit()
        flash('You have successfully edited the speciality.')

        # Reirect to the teachers page.
        return redirect(url_for('admin.list_teachers'))
    
    form.speciality.data = teacher.speciality
    return render_template(
        'admin/teachers/teacher.html', 
        action="Edit",
        form=form,
        teacher=teacher,
        title="Edit Teacher"
    )

@admin.route('/teachers/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_teacher(id):
    '''
    Delete a teacher from the database.
    '''

    check_admin()

    teacher = Teacher.query.get_or_404(id)
    db.session.delete(teacher)
    db.session.commit()
    flash('You have successfully deleted the teacher.')

    # Redirect to the teachers page.
    return redirect(url_for('admin.list_teachers'))

    return render_template(title="Delete Teacher")

# Verification View.

@admin.route('/unverified_users', methods=['GET', 'POST'])
@login_required
def list_unverified_users():
    '''
    List all unverified users.
    '''

    check_admin()

    # Fetch all unverified users.
    unverified_users = User.query.filter_by(status=False).all()
    
    return render_template(
        'admin/user_verification/unverified_users.html', 
        unverified_users=unverified_users,
        title="Unverified Users"
    )

@admin.route('/unverified_users/verify_user/<int:id>', methods=['GET', 'POST'])
@login_required
def verify_user(id):
    '''
    Verify a specific user by ID.
    '''

    check_admin()

    user = User.query.get_or_404(id)
    form = VerifyUserForm(obj=user)
    if form.validate_on_submit():
        user.status = True
        db.session.commit()
        flash('User successfully verified.')

        # Redirect to unverified users page.
        return redirect(url_for('admin.list_unverified_users'))
    
    return render_template(
        'admin/user_verification/verify_user.html',
        form=form,
        user=user,
        title="Verify User"
    )
