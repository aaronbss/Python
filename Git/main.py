from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:Anthony10c1997@sneaker.c6x6z62swbhb.eu-west-1.rds.amazonaws.com'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    #date_created = db.Column(db.DateTime, default=datetime.now)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


@app.route('/<name>/<name1>')
def index(name, name1):
    user = User(name=name)
    db.session.add(user)
    db.session.commit()
    student = Student(name=name1)
    db.session.add(student)
    db.session.commit()
    return '<h1>Added New User!</h1>'


@app.route('/<name>')
def get_user(name):
    user = User.query.filter_by(name=name).first()

    return f'<h1>The name and ID are: {user.name} , {user.id}</h1>'


if __name__ == '__main__':
    app.run()
