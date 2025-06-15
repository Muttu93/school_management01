from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
import webbrowser

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
db = SQLAlchemy(app)

# Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    standard = db.Column(db.String(50))
    fees_paid = db.Column(db.String(10))
    activity = db.Column(db.String(200))
    marks = db.Column(db.String(50))

# Staff model
class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    subject = db.Column(db.String(100))
    salary = db.Column(db.String(50))
    attendance = db.Column(db.String(100))

# Committee model
class Committee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    role = db.Column(db.String(100))
    expenditure = db.Column(db.String(100))

# Finance model
class Finance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_income = db.Column(db.String(100))
    total_expense = db.Column(db.String(100))
    description = db.Column(db.String(200))

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

@app.route('/logout')
def logout():
    flash('You have been logged out successfully!')
    return redirect(url_for('login'))

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/students")
def students():
    students = Student.query.all()
    return render_template('students.html', students=students)

@app.route("/add_student", methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        standard = request.form['standard']
        fees_paid = request.form['fees_paid']
        activity = request.form['activity']
        marks = request.form['marks']
        student = Student(name=name, standard=standard, fees_paid=fees_paid, activity=activity, marks=marks)
        db.session.add(student)
        db.session.commit()
        flash('Student added successfully!')
        return redirect(url_for('students'))
    return render_template('add_student.html')

@app.route("/edit_student/<int:id>", methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get(id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.standard = request.form['standard']
        student.fees_paid = request.form['fees_paid']
        student.activity = request.form['activity']
        student.marks = request.form['marks']
        db.session.commit()
        flash('Student updated successfully!')
        return redirect(url_for('students'))
    return render_template('add_student.html', student=student)

@app.route("/delete_student/<int:id>")
def delete_student(id):
    student = Student.query.get(id)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted successfully!')
    return redirect(url_for('students'))

# Staff Routes
@app.route("/staff")
def staff():
    staff = Staff.query.all()
    return render_template('staff.html', staff=staff)

@app.route("/add_staff", methods=['GET', 'POST'])
def add_staff():
    if request.method == 'POST':
        name = request.form['name']
        subject = request.form['subject']
        salary = request.form['salary']
        attendance = request.form['attendance']
        staff_member = Staff(name=name, subject=subject, salary=salary, attendance=attendance)
        db.session.add(staff_member)
        db.session.commit()
        flash('Staff added successfully!')
        return redirect(url_for('staff'))
    return render_template('add_staff.html')

@app.route("/edit_staff/<int:id>", methods=['GET', 'POST'])
def edit_staff(id):
    staff_member = Staff.query.get(id)
    if request.method == 'POST':
        staff_member.name = request.form['name']
        staff_member.subject = request.form['subject']
        staff_member.salary = request.form['salary']
        staff_member.attendance = request.form['attendance']
        db.session.commit()
        flash('Staff updated successfully!')
        return redirect(url_for('staff'))
    return render_template('add_staff.html', staff=staff_member)

@app.route("/delete_staff/<int:id>")
def delete_staff(id):
    staff_member = Staff.query.get(id)
    db.session.delete(staff_member)
    db.session.commit()
    flash('Staff deleted successfully!')
    return redirect(url_for('staff'))

# Committee Routes
@app.route("/committee")
def committee():
    committee = Committee.query.all()
    return render_template('committee.html', committee=committee)

@app.route("/add_committee", methods=['GET', 'POST'])
def add_committee():
    if request.method == 'POST':
        name = request.form['name']
        role = request.form['role']
        expenditure = request.form['expenditure']
        committee_member = Committee(name=name, role=role, expenditure=expenditure)
        db.session.add(committee_member)
        db.session.commit()
        flash('Committee member added successfully!')
        return redirect(url_for('committee'))
    return render_template('add_committee.html')

@app.route("/edit_committee/<int:id>", methods=['GET', 'POST'])
def edit_committee(id):
    committee_member = Committee.query.get(id)
    if request.method == 'POST':
        committee_member.name = request.form['name']
        committee_member.role = request.form['role']
        committee_member.expenditure = request.form['expenditure']
        db.session.commit()
        flash('Committee member updated successfully!')
        return redirect(url_for('committee'))
    return render_template('add_committee.html', committee=committee_member)

@app.route("/delete_committee/<int:id>")
def delete_committee(id):
    committee_member = Committee.query.get(id)
    db.session.delete(committee_member)
    db.session.commit()
    flash('Committee member deleted successfully!')
    return redirect(url_for('committee'))

# Finance Routes
@app.route("/finance")
def finance():
    finance = Finance.query.all()
    return render_template('finance.html', finance=finance)

@app.route("/add_finance", methods=['GET', 'POST'])
def add_finance():
    if request.method == 'POST':
        total_income = request.form['total_income']
        total_expense = request.form['total_expense']
        description = request.form['description']
        finance_record = Finance(total_income=total_income, total_expense=total_expense, description=description)
        db.session.add(finance_record)
        db.session.commit()
        flash('Finance record added successfully!')
        return redirect(url_for('finance'))
    return render_template('add_finance.html')

@app.route("/edit_finance/<int:id>", methods=['GET', 'POST'])
def edit_finance(id):
    finance_record = Finance.query.get(id)
    if request.method == 'POST':
        finance_record.total_income = request.form['total_income']
        finance_record.total_expense = request.form['total_expense']
        finance_record.description = request.form['description']
        db.session.commit()
        flash('Finance record updated successfully!')
        return redirect(url_for('finance'))
    return render_template('add_finance.html', finance=finance_record)

@app.route("/delete_finance/<int:id>")
def delete_finance(id):
    finance_record = Finance.query.get(id)
    db.session.delete(finance_record)
    db.session.commit()
    flash('Finance record deleted successfully!')
    return redirect(url_for('finance'))

# Auto open browser
@app.before_first_request
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == "__main__":
    if not os.path.exists('school.db'):
        db.create_all()
    app.run(debug=True)
