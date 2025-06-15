from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os
import webbrowser

# Flask app setup
app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to something secure

# File upload configuration
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database setup
db = SQLAlchemy(app)

# Student Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    standard = db.Column(db.String(50))
    fee_status = db.Column(db.String(20))
    activities = db.Column(db.Text)
    marks = db.Column(db.String(20))
    file = db.Column(db.String(100))

# Staff Model
class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    subject = db.Column(db.String(100))
    salary = db.Column(db.String(50))
    attendance = db.Column(db.String(20))

# Committee Model
class Committee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    role = db.Column(db.String(100))
    expenditure = db.Column(db.String(50))

# Finance Model
class Finance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fees_collected = db.Column(db.String(50))
    expenses = db.Column(db.String(50))
    turnover = db.Column(db.String(50))

# Home / Login
@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        if user == 'admin' and pwd == 'admin':
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials. Try again.')
    return render_template('login.html')

# Home Page (School Introduction)
@app.route("/home")
def home():
    return render_template('home.html')

# Student CRUD
@app.route("/students")
def students():
    students = Student.query.all()
    return render_template('students.html', students=students)

@app.route("/add_student", methods=['POST'])
def add_student():
    name = request.form['name']
    standard = request.form['standard']
    fee_status = request.form['fee_status']
    activities = request.form['activities']
    marks = request.form['marks']
    file = request.files['file']
    filename = ""
    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    student = Student(name=name, standard=standard, fee_status=fee_status,
                      activities=activities, marks=marks, file=filename)
    db.session.add(student)
    db.session.commit()
    flash('Student added successfully!')
    return redirect(url_for('students'))

@app.route("/edit_student/<int:id>", methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get(id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.standard = request.form['standard']
        student.fee_status = request.form['fee_status']
        student.activities = request.form['activities']
        student.marks = request.form['marks']
        file = request.files['file']
        if file and file.filename != '':
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            student.file = filename
        db.session.commit()
        flash('Student updated successfully!')
        return redirect(url_for('students'))
    return render_template('edit_student.html', student=student)

@app.route("/delete_student/<int:id>")
def delete_student(id):
    student = Student.query.get(id)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted successfully!')
    return redirect(url_for('students'))

# Staff CRUD
@app.route("/staff")
def staff():
    staff = Staff.query.all()
    return render_template('sta_
