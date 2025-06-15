from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import webbrowser

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    standard = db.Column(db.String(50))
    admission_fee_paid = db.Column(db.Boolean, default=False)
    activities = db.Column(db.String(200))
    marks = db.Column(db.String(50))
    extra_fee = db.Column(db.Float)
    parent_notification = db.Column(db.String(200))
    attendance = db.Column(db.String(50))

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    subject = db.Column(db.String(100))
    salary = db.Column(db.Float)
    attendance = db.Column(db.String(50))

class Committee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_name = db.Column(db.String(100))
    role = db.Column(db.String(100))
    expenditure = db.Column(db.Float)

class Finance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_income = db.Column(db.Float)
    total_expenditure = db.Column(db.Float)

# Routes
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == 'admin':
        return redirect(url_for('home'))
    else:
        return 'Invalid Credentials!'

@app.route('/logout')
def logout():
    return redirect(url_for('login'))

@app.route('/home')
def home():
    return render_template('home.html')

# Student CRUD
@app.route('/students')
def students():
    students = Student.query.all()
    return render_template('students.html', students=students)

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form['name']
    standard = request.form['standard']
    admission_fee_paid = 'admission_fee_paid' in request.form
    activities = request.form['activities']
    marks = request.form['marks']
    extra_fee = float(request.form['extra_fee'])
    parent_notification = request.form['parent_notification']
    attendance = request.form['attendance']
    student = Student(name=name, standard=standard, admission_fee_paid=admission_fee_paid,
                      activities=activities, marks=marks, extra_fee=extra_fee,
                      parent_notification=parent_notification, attendance=attendance)
    db.session.add(student)
    db.session.commit()
    return redirect(url_for('students'))

@app.route('/update_student/<int:id>', methods=['POST'])
def update_student(id):
    student = Student.query.get(id)
    student.name = request.form['name']
    student.standard = request.form['standard']
    student.admission_fee_paid = 'admission_fee_paid' in request.form
    student.activities = request.form['activities']
    student.marks = request.form['marks']
    student.extra_fee = float(request.form['extra_fee'])
    student.parent_notification = request.form['parent_notification']
    student.attendance = request.form['attendance']
    db.session.commit()
    return redirect(url_for('students'))

@app.route('/delete_student/<int:id>')
def delete_student(id):
    student = Student.query.get(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('students'))

# Staff CRUD
@app.route('/staff')
def staff():
    staff_list = Staff.query.all()
    return render_template('staff.html', staff=staff_list)

@app.route('/add_staff', methods=['POST'])
def add_staff():
    name = request.form['name']
    subject = request.form['subject']
    salary = float(request.form['salary'])
    attendance = request.form['attendance']
    staff = Staff(name=name, subject=subject, salary=salary, attendance=attendance)
    db.session.add(staff)
    db.session.commit()
    return redirect(url_for('staff'))

@app.route('/update_staff/<int:id>', methods=['POST'])
def update_staff(id):
    staff = Staff.query.get(id)
    staff.name = request.form['name']
    staff.subject = request.form['subject']
    staff.salary = float(request.form['salary'])
    staff.attendance = request.form['attendance']
    db.session.commit()
    return redirect(url_for('staff'))

@app.route('/delete_staff/<int:id>')
def delete_staff(id):
    staff = Staff.query.get(id)
    db.session.delete(staff)
    db.session.commit()
    return redirect(url_for('staff'))

# Committee CRUD
@app.route('/committee')
def committee():
    committee_list = Committee.query.all()
    return render_template('committee.html', committee=committee_list)

@app.route('/add_committee', methods=['POST'])
def add_committee():
    member_name = request.form['member_name']
    role = request.form['role']
    expenditure = float(request.form['expenditure'])
    committee = Committee(member_name=member_name, role=role, expenditure=expenditure)
    db.session.add(committee)
    db.session.commit()
    return redirect(url_for('committee'))

@app.route('/update_committee/<int:id>', methods=['POST'])
def update_committee(id):
    committee = Committee.query.get(id)
    committee.member_name = request.form['member_name']
    committee.role = request.form['role']
    committee.expenditure = float(request.form['expenditure'])
    db.session.commit()
    return redirect(url_for('committee'))

@app.route('/delete_committee/<int:id>')
def delete_committee(id):
    committee = Committee.query.get(id)
    db.session.delete(committee)
    db.session.commit()
    return redirect(url_for('committee'))

# Finance CRUD
@app.route('/finance')
def finance():
    finance_list = Finance.query.all()
    return render_template('finance.html', finance=finance_list)

@app.route('/add_finance', methods=['POST'])
def add_finance():
    total_income = float(request.form['total_income'])
    total_expenditure = float(request.form['total_expenditure'])
    finance = Finance(total_income=total_income, total_expenditure=total_expenditure)
    db.session.add(finance)
    db.session.commit()
    return redirect(url_for('finance'))

@app.route('/update_finance/<int:id>', methods=['POST'])
def update_finance(id):
    finance = Finance.query.get(id)
    finance.total_income = float(request.form['total_income'])
    finance.total_expenditure = float(request.form['total_expenditure'])
    db.session.commit()
    return redirect(url_for('finance'))

@app.route('/delete_finance/<int:id>')
def delete_finance(id):
    finance = Finance.query.get(id)
    db.session.delete(finance)
    db.session.commit()
    return redirect(url_for('finance'))

# Run with auto browser open
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Auto create school.db
    webbrowser.open('http://127.0.0.1:5000/')  # Auto browser open
    app.run(debug=True)
