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
    return render_template('staff.html', staff=staff)

@app.route("/add_staff", methods=['POST'])
def add_staff():
    name = request.form['name']
    subject = request.form['subject']
    salary = request.form['salary']
    attendance = request.form['attendance']
    staff_member = Staff(name=name, subject=subject, salary=salary, attendance=attendance)
    db.session.add(staff_member)
    db.session.commit()
    flash('Staff member added!')
    return redirect(url_for('staff'))

@app.route("/edit_staff/<int:id>", methods=['GET', 'POST'])
def edit_staff(id):
    staff_member = Staff.query.get(id)
    if request.method == 'POST':
        staff_member.name = request.form['name']
        staff_member.subject = request.form['subject']
        staff_member.salary = request.form['salary']
        staff_member.attendance = request.form['attendance']
        db.session.commit()
        flash('Staff member updated!')
        return redirect(url_for('staff'))
    return render_template('edit_staff.html', staff=staff_member)

@app.route("/delete_staff/<int:id>")
def delete_staff(id):
    staff_member = Staff.query.get(id)
    db.session.delete(staff_member)
    db.session.commit()
    flash('Staff member deleted!')
    return redirect(url_for('staff'))

# Committee CRUD
@app.route("/committee")
def committee():
    committee = Committee.query.all()
    return render_template('committee.html', committee=committee)

@app.route("/add_committee", methods=['POST'])
def add_committee():
    name = request.form['name']
    role = request.form['role']
    expenditure = request.form['expenditure']
    committee_member = Committee(name=name, role=role, expenditure=expenditure)
    db.session.add(committee_member)
    db.session.commit()
    flash('Committee member added!')
    return redirect(url_for('committee'))

@app.route("/edit_committee/<int:id>", methods=['GET', 'POST'])
def edit_committee(id):
    committee_member = Committee.query.get(id)
    if request.method == 'POST':
        committee_member.name = request.form['name']
        committee_member.role = request.form['role']
        committee_member.expenditure = request.form['expenditure']
        db.session.commit()
        flash('Committee member updated!')
        return redirect(url_for('committee'))
    return render_template('edit_committee.html', committee=committee_member)

@app.route("/delete_committee/<int:id>")
def delete_committee(id):
    committee_member = Committee.query.get(id)
    db.session.delete(committee_member)
    db.session.commit()
    flash('Committee member deleted!')
    return redirect(url_for('committee'))

# Finance CRUD
@app.route("/finance")
def finance():
    finance = Finance.query.all()
    return render_template('finance.html', finance=finance)

@app.route("/add_finance", methods=['POST'])
def add_finance():
    fees_collected = request.form['fees_collected']
    expenses = request.form['expenses']
    turnover = request.form['turnover']
    finance_entry = Finance(fees_collected=fees_collected, expenses=expenses, turnover=turnover)
    db.session.add(finance_entry)
    db.session.commit()
    flash('Finance record added!')
    return redirect(url_for('finance'))

@app.route("/edit_finance/<int:id>", methods=['GET', 'POST'])
def edit_finance(id):
    finance_entry = Finance.query.get(id)
    if request.method == 'POST':
        finance_entry.fees_collected = request.form['fees_collected']
        finance_entry.expenses = request.form['expenses']
        finance_entry.turnover = request.form['turnover']
        db.session.commit()
        flash('Finance record updated!')
        return redirect(url_for('finance'))
    return render_template('edit_finance.html', finance=finance_entry)

@app.route("/delete_finance/<int:id>")
def delete_finance(id):
    finance_entry = Finance.query.get(id)
    db.session.delete(finance_entry)
    db.session.commit()
    flash('Finance record deleted!')
    return redirect(url_for('finance'))

# File Download
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Run and auto open browser
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    port = 5000
    url = f"http://127.0.0.1:{port}"
    print(f"Server running on {url}")
    webbrowser.open(url)
    app.run(debug=True, port=port)
