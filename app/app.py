import time
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:example@db:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.init_app(app)

class students(db.Model):
    __tablename__ = 'students'
    id = db.Column('student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))

    def __init__(self, name, city, addr):
        self.name = name
        self.city = city
        self.addr = addr

def database_initialization_sequence():
    db.create_all()
    test_rec = students(
            'John Doe',
            'Los Angeles',
            '123 Foobar Ave')

    db.session.add(test_rec)
    db.session.rollback()
db.session.commit()


@app.route('/')
def view_all():
    result = students.query.all()
    return render_template('students_overview.html', data=result)

@app.route('/register', methods = ['GET'])
def view_registration_form():
    return render_template('student_registration.html')

@app.route('/register', methods = ['POST'])
def register_student():
    name = request.form.get('name')
    city = request.form.get('city')
    addr = request.form.get('addr')
    student = students(name, city, addr)
    db.session.add(student)
    db.session.commit()
    # flash('Record was succesfully added')
    #all_students = students.query.all()
    return render_template('student_confirmation.html', name=name, city=city, addr=addr)


if __name__ == "__main__":
    dbstatus = False
    while dbstatus == False:
        try:
            db.create_all()   
        except:
            time.sleep(2)
        else:
            dbstatus = True
    database_initialization_sequence()
    app.run(host="0.0.0.0", debug=True)
    

