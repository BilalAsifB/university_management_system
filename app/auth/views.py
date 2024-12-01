# app/auth/views.py

from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from .forms import LoginForm, RegistrationForm
from . import auth
from .. import db
from ..models import User, Student, Teacher

@auth.route('/register', methods=['GET', 'POST'])
def register():
    '''
    Handle requests to the /register route.
    Add a user to the database through the registration form.
    '''

    form = RegistrationForm()
    if form.validate_on_submit():
        flag = form.role.data == "Admin"
            
        user = User(
            email=form.email.data,
            username=form.username.data,
            _password=form.password.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            contact=form.contact.data,
            address=form.address.data,
            role=form.role.data,
            is_admin=flag
        )

        # Add user to the database.
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!')

        if form.role.data == 'Student':
            student = Student(
                user_id=user.id,
                department_id=None
            )

            # Add student to the database.
            db.session.add(student)
            db.session.commit()

        elif form.role.data == 'Teacher':
            teacher = Teacher(
                user_id=user.id,
                speciality=None
            )

            # Add teacher to the database.
            db.session.add(teacher)
            db.session.commit()

        # Redirect to the login page.
        return redirect(url_for('auth.login'))
    
    # Load registration template.
    return render_template('auth/register.html', form=form, title='Register')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Handle requests to the /login route.
    Log a user in through the login form
    '''

    form = LoginForm()
    if form.validate_on_submit():

        # Check whether user exists in the database and whether the 
        # password entered matches the password in the database.
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):

            # Log user in.
            login_user(user)

            # Redirect to the appropriate dashboard page.
            if user.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            else:
                return redirect(url_for('home.dashboard'))
            
        # When login details are incorrect.
        else:
            flash('Invalid email or password!')
    
    # Load login template.
    return render_template('auth/login.html', form=form, title='Login')

@auth.route('/logout')
@login_required
def logout():
    '''
    Handle requests to the /logout route.
    Log a user out through the logout link.
    '''

    logout_user()
    flash('Logged out successful!')

    # Redirect to the login page.
    return redirect(url_for('auth.login'))
