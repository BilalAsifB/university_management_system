from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class User(UserMixin, db.Model):
    '''
    Create a User table.
    '''
    __tablename__ = 'users'
    id_seq = db.Sequence('id_seq', start=1, increment=1)
    id = db.Column(db.Integer, id_seq, server_default=id_seq.next_value(), primary_key=True)
    
    email = db.Column(db.String(50), unique=True, nullable=False, index=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    _password = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    contact = db.Column(db.String(50), unique=True, nullable=False, index=True)
    address = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    status = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        '''
        Prevent password from being accessed.
        '''
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        '''
        Set password to a hashed password.
        '''
        # print('-----> ', generate_password_hash(password))
        self._password = generate_password_hash(password)

    def verify_password(self, password):
        '''
        Check if hashed password matches actual password.
        '''
        print(self._password, password)
        # return check_password_hash(self._password, password)
        return self._password == password

    def __repr__(self):
        return f'<User: {self.username}>'

    # Check constraints
    __table_args__ = (
        db.CheckConstraint("role IN ('Student', 'Teacher', 'Admin')", name='check_role_valid'),
    )

    # Relationships
    students = db.relationship("Student", back_populates="users", single_parent=True, uselist=False, cascade="all, delete-orphan")
    teachers = db.relationship("Teacher", back_populates="users", single_parent=True, uselist=False, cascade="all, delete-orphan")


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Student(db.Model):
    '''
    Create a Student table.
    '''
    __tablename__ = 'students'
    roll_no_seq = db.Sequence('roll_no_seq', start=1, increment=1)
    roll_no = db.Column(db.Integer, roll_no_seq, server_default=roll_no_seq.next_value(), primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.dep_id'))
    
    # Relationships
    users = db.relationship("User", back_populates="students", single_parent=True, cascade="all, delete-orphan")
    enrollments = db.relationship("Enrollment", back_populates="students", lazy=True, cascade="all, delete-orphan")
    fees = db.relationship("Fee", back_populates="students", lazy=True, cascade="all, delete-orphan")
    departments = db.relationship("Department", back_populates="students", lazy=True)

    def __repr__(self):
        return f'<Student: {self.first_name}>'


class Teacher(db.Model):
    '''
    Create Teacher table.
    '''
    __tablename__ = 'teachers'
    teacher_id_seq = db.Sequence('teacher_id_seq', start=1, increment=1)
    teacher_id = db.Column(db.Integer, teacher_id_seq, server_default=teacher_id_seq.next_value(), primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    speciality = db.Column(db.String(50))

    # Check constraints
    __table_args__ = (
        db.CheckConstraint("speciality IN ('CS', 'NS', 'AI', 'EE', 'MG', 'MT')", name='check_speciality_valid'),
    )

    # Relationships
    users = db.relationship("User", back_populates="teachers", single_parent=True, uselist=False, cascade="all, delete-orphan")
    courses = db.relationship("Course", back_populates="teachers", lazy=True)

    def __repr__(self):
        return f'<Teacher: {self.first_name}>'


class Course(db.Model):
    '''
    Create a Course table.
    '''
    __tablename__ = 'courses'
    course_id_seq = db.Sequence('course_id_seq', start=1, increment=1)
    course_id = db.Column(db.Integer, course_id_seq, server_default=course_id_seq.next_value(), primary_key=True)

    course_name = db.Column(db.String(100), unique=True, nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.teacher_id'))

    # Check constraints
    __table_args__ = (
        db.CheckConstraint("credits BETWEEN 1 AND 3", name='check_credits_range'),
    )

    # Relationships
    teachers = db.relationship("Teacher", back_populates="courses", lazy=True)
    enrollments = db.relationship("Enrollment", back_populates="courses", lazy=True, cascade="all, delete-orphan")
    fees = db.relationship("Fee", back_populates="courses", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Course: {self.course_name}>'


class Enrollment(db.Model):
    '''
    Create an Enrollment table.
    '''
    __tablename__ = 'enrollments'
    enrollment_id_seq = db.Sequence('enrollment_id_seq', start=1, increment=1)
    enrollment_id = db.Column(db.Integer, enrollment_id_seq, server_default=enrollment_id_seq.next_value(), primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey('students.roll_no'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'))

    # Relationships
    students = db.relationship("Student", back_populates="enrollments", lazy=True)
    courses = db.relationship("Course", back_populates="enrollments", lazy=True)

    def __repr__(self):
        return f'<Enrollment: Student {self.student_id}, Course {self.course_id}>'


class Fee(db.Model):
    '''
    Create a Fee table.
    '''
    __tablename__ = 'fees'
    fee_id_seq = db.Sequence('fee_id_seq', start=1, increment=1)
    fee_id = db.Column(db.Integer, fee_id_seq, server_default=fee_id_seq.next_value(), primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey('students.roll_no'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'))
    amount = db.Column(db.Float, nullable=False)
    fee_status = db.Column(db.String(10), nullable=False)

    # Check constraints
    __table_args__ = (
        db.CheckConstraint("fee_status IN ('Paid', 'Pending')", name='check_fee_status_valid'),
    )

    # Relationships
    students = db.relationship("Student", back_populates="fees", lazy=True)
    courses = db.relationship("Course", back_populates="fees", lazy=True)

    def __repr__(self):
        return f'<Fee: Student {self.student_id}, Course {self.course_id}>'


class Department(db.Model):
    '''
    Create a Department table.
    '''
    __tablename__ = 'departments'
    dep_id_seq = db.Sequence('dep_id_seq', start=1, increment=1)
    dep_id = db.Column(db.Integer, dep_id_seq, server_default=dep_id_seq.next_value(), primary_key=True)

    dep_name = db.Column(db.String(100), unique=True, nullable=False)

    # Check constraints
    __table_args__ = (
        db.CheckConstraint("dep_name IN ('CS', 'SE', 'AI', 'CYS', 'EE')", name='check_dep_name_valid'),
    )

    # Relationships
    students = db.relationship("Student", back_populates="departments", lazy=True)

    def __repr__(self):
        return f'<Department: {self.dep_name}>'

# class Grade(db.Model):
#     __tablename__ = 'grade'
#     grade_id = db.Column(db.Integer, primary_key=True)
#     enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollment.enrollment_id'))
#     marks = db.Column(db.Integer)
#     grade = db.Column(db.String(2))
    
#     __table_args__ = (
#         db.CheckConstraint("marks BETWEEN 1 AND 100", 
#                            name='check_marks_range'),
#         db.CheckConstraint("grade IN ('F', 'D-', 'D', 'D+', 'C-', 'C', 'C+', 'B-', 'B', 'B+', 'A-', 'A', 'A+')",
#                            NAME='check_grade_valid')
#     )
#     # Relationships
#     enrollment = db.relationship("Enrollment", back_populates="grade", lazy=True)

# class Attendance(db.Model):
#     __tablename__ = 'attendance'
#     attendance_id = db.Column(db.Integer, primary_key=True)
#     enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollment.enrollment_id'))
#     date = db.Column(db.Date, nullable=False)
#     status = db.Column(db.String(2), nullable=False)
#     __table_args__ = (
#         db.CheckConstraint("status IN ('P', 'A', 'L')", 
#                            name='check_status_valid'),
#     )
    
#     # Relationships
#     enrollment = db.relationship("Enrollment", back_populates="attendance", lazy=True)
