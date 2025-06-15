# app.py (Complete Backend for School Management System)

from flask import Flask, render_template, redirect, url_for, request, flash, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db = SQLAlchemy(app)

# Models
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    standard = db.Column(db.String(10))
    fee_status = db.Column(db.String(20))
    activities = db.Column(db.String(200))
    marks = db.Column(db.String(10))
    file = db.Column(db.String(200))

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    subject = db.Column(db.String(100))
    salary = db.Column(db.Integer)
    attendance = db.Column(db.String(100))

class Committee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    role = db.Column(db.String(100))
    expenditure = db.Column(db.Integer)

# Routes
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            session['user'] = 'admin'
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/students', methods=['GET', 'POST'])
def students():
    if 'user' not in session:
        return redirect(url_for('login'))
    search = request.args.get('search')
    standard = request.args.get('standard')
    if search:
        student_list = Student.query.filter(Student.name.like(f'%{search}%')).all()
    elif standard:
        student_list = Student.query.filter_by(standard=standard).all()
    else:
        student_list = Student.query.all()
    return render_template('students.html', students=student_list)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        new_student = Student(
            name=request.form['name'],
            standard=request.form['standard'],
            fee_status=request.form['fee_status'],
            activities=request.form['activities'],
            marks=request.form['marks'],
            file=filename
        )
        db.session.add(new_student)
        db.session.commit()
        flash('Student added successfully')
        return redirect(url_for('students'))
    return render_template('add_student.html')

@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.standard = request.form['standard']
        student.fee_status = request.form['fee_status']
        student.activities = request.form['activities']
        student.marks = request.form['marks']
        file = request.files.get('file')
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            student.file = filename
        db.session.commit()
        flash('Student updated successfully')
        return redirect(url_for('students'))
    return render_template('edit_student.html', student=student)

@app.route('/delete_student/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted successfully')
    return redirect(url_for('students'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Staff Management
@app.route('/staff')
def staff():
    staff_list = Staff.query.all()
    return render_template('staff.html', staff=staff_list)

@app.route('/add_staff', methods=['GET', 'POST'])
def add_staff():
    if request.method == 'POST':
        new_staff = Staff(
            name=request.form['name'],
            subject=request.form['subject'],
            salary=request.form['salary'],
            attendance=request.form['attendance']
        )
        db.session.add(new_staff)
        db.session.commit()
        flash('Staff added successfully')
        return redirect(url_for('staff'))
    return render_template('add_staff.html')

@app.route('/edit_staff/<int:id>', methods=['GET', 'POST'])
def edit_staff(id):
    staff = Staff.query.get_or_404(id)
    if request.method == 'POST':
        staff.name = request.form['name']
        staff.subject = request.form['subject']
        staff.salary = request.form['salary']
        staff.attendance = request.form['attendance']
        db.session.commit()
        flash('Staff updated successfully')
        return redirect(url_for('staff'))
    return render_template('edit_staff.html', staff=staff)

@app.route('/delete_staff/<int:id>')
def delete_staff(id):
    staff = Staff.query.get_or_404(id)
    db.session.delete(staff)
    db.session.commit()
    flash('Staff deleted successfully')
    return redirect(url_for('staff'))

# Committee Management
@app.route('/committee')
def committee():
    committee_list = Committee.query.all()
    return render_template('committee.html', committee=committee_list)

@app.route('/add_committee', methods=['GET', 'POST'])
def add_committee():
    if request.method == 'POST':
        new_committee = Committee(
            name=request.form['name'],
            role=request.form['role'],
            expenditure=request.form['expenditure']
        )
        db.session.add(new_committee)
        db.session.commit()
        flash('Committee Member added successfully')
        return redirect(url_for('committee'))
    return render_template('add_committee.html')

@app.route('/edit_committee/<int:id>', methods=['GET', 'POST'])
def edit_committee(id):
    committee = Committee.query.get_or_404(id)
    if request.method == 'POST':
        committee.name = request.form['name']
        committee.role = request.form['role']
        committee.expenditure = request.form['expenditure']
        db.session.commit()
        flash('Committee Member updated successfully')
        return redirect(url_for('committee'))
    return render_template('edit_committee.html', committee=committee)

@app.route('/delete_committee/<int:id>')
def delete_committee(id):
    committee = Committee.query.get_or_404(id)
    db.session.delete(committee)
    db.session.commit()
    flash('Committee Member deleted successfully')
    return redirect(url_for('committee'))

# Finance Page
@app.route('/finance')
def finance():
    total_fees = 0
    total_expenses = 0
    students = Student.query.all()
    committee = Committee.query.all()

    for s in students:
        if s.fee_status.lower() == 'paid':
            total_fees += 10000  # example: each student fee assumed as 10,000
    for c in committee:
        total_expenses += c.expenditure

    turnover = total_fees - total_expenses
    return render_template('finance.html', fees=total_fees, expenses=total_expenses, turnover=turnover)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
