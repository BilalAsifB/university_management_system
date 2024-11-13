from app import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=True, nullable=False)
    contact = db.Columns(db.String(50), unique=True, nullable=False)
    address = db.Columns(db.String(200), nullable=False)
    role = db.Columns(db.String(100), nullable=False)

    __table_args__ = (
        db.CheckConstraint("role IN ('Student', 'Teacher', 'Admin')", 
                           name='check_role_valid'),
        db.CheckConstraint("(role != 'Admin') OR (SELECT COUNT(*) FROM user WHERE role = 'admin') <= 1",
                           name='check_only_single_admin')
    )

    # Relationships
    student = db.relationship("Student", back_populates="user", uselist=False)
    teacher = db.relationship("Teacher", back_populates="user", uselist=False)

class Student(db.Model):
    __tablename__ = 'student'
    roll_no = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    department_id = db.column(db.Integer, db.ForeignKey('department.dep_id'))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    
    # Relationships
    user = db.relationship("User", back_populates="student")
    enrollment = db.relationship("Enrollment", back_populates="student", lazy=True)
    fee = db.relationship("Fee", back_populates="student", lazy=True)
    fee_summary = db.relationship("FeeSummary", back_populates="student", uselist=False)
    department = db.relationship("Department", back_populates="student", lazy=True)

class Teacher(db.Model):
    __tablename__ = 'teacher'
    teacher_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    
    # Relationships
    user = db.relationship("User", back_populates="teacher")
    course = db.relationship("Course", back_populates="teacher", lazy=True)

class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), unique=True, nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.teacher_id'))
    
    __table_args__ = (
        db.CheckConstraint("credits BETWEEEN 1 AND 3", 
                           name='check_credits_range'),
    )

    # Relationships
    teacher = db.relationship("Teacher", back_populates="course", lazy=True)
    enrollment = db.relationship("Enrollment", back_populates="course", lazy=True)

class Enrollment(db.Model):
    __tablename__ = 'enrollment'
    enrollment_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.roll_no'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'))
    
    # Relationships
    student = db.relationship("Student", back_populates="enrollment", lazy=True)
    course = db.relationship("Course", back_populates="enrollment", lazy=True)
    grade = db.relationship("Grade", back_populates="enrollment", uselist=False)
    attendance = db.relationship("Attendance", back_populates="enrollment", lazy=True)

class Grade(db.Model):
    __tablename__ = 'grade'
    grade_id = db.Column(db.Integer, primary_key=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollment.enrollment_id'))
    marks = db.Column(db.Integer)
    grade = db.Column(db.String(2))
    
    __table_args__ = (
        db.CheckConstraint("marks BETWEEN 1 AND 100", 
                           name='check_marks_range'),
        db.CheckConstraint("grade IN ('F', 'D-', 'D', 'D+', 'C-', 'C', 'C+', 'B-', 'B', 'B+', 'A-', 'A', 'A+')",
                           NAME='check_grade_valid')
    )

    # Relationships
    enrollment = db.relationship("Enrollment", back_populates="grade", lazy=True)

class Attendance(db.Model):
    __tablename__ = 'attendance'
    attendance_id = db.Column(db.Integer, primary_key=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollment.enrollment_id'))
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(2), nullable=False)

    __table_args__ = (
        db.CheckConstraint("status IN ('P', 'A', 'L')", 
                           name='check_status_valid'),
    )
    
    # Relationships
    enrollment = db.relationship("Enrollment", back_populates="attendance", lazy=True)

class Fee(db.Model):
    __tablename__ = 'fee'
    fee_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.roll_no'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'))    
    amount = db.Column(db.Float, nullable=False)
    
    # Relationships
    student = db.relationship("Student", back_populates="fee", lazy=True)

class FeeSummary(db.Model):
    __tablename__ = 'fee_summary'
    summary_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.roll_no'))
    total_fees_due = db.Column(db.Float, nullable=False)
    fee_status = db.Column(db.String(10), nullable=False)

    __table_args__ = (
        db.CheckConstraint("status IN ('Paid', 'Pending')", 
                           name='check_status_valid'),
    )
    
    # Relationships
    student = db.relationship("Student", back_populates="fee_summary")

class Department(db.Model):
    __tablename__ = 'department'
    dep_id = db.Column(db.Integer, primary_key=True)
    dep_name = db.Column(db.String(100), unique=True, nullable=False)
    
    # Relationships
    student = db.relationship("Student", back_populates="department", lazy=True)