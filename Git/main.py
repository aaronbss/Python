from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.Electronics'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:Anthony10c1997@sneaker.c6x6z62swbhb.eu-west-1.rds.amazonaws.com'
db = SQLAlchemy(app)


def _get_date():
    return datetime.datetime.now()


class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    designation = db.Column(db.String(100))
    order = relationship("Orders", backref="employee")


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    category = db.Column(db.String(50))
    description = db.Column(db.String(200))
    barcode = db.Column(db.Integer)
    price = db.Column(db.Integer)
    warehouse = relationship("Warehouse", backref="product")


class Orders(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    product_IDs = db.Column(db.String(200))
    quantity = db.Column(db.Integer)
    total_cost = db.Column(db.Integer)
    billed_at = db.Column(db.Date, default=_get_date)
    emp_ID = db.Column(db.Integer, db.ForeignKey('employee.id'))


class Warehouse(db.Model):
    __tablename__ = 'warehouse'
    Shipment_ID = db.Column(db.Integer, primary_key=True)
    Product_ID = db.Column(db.Integer, db.ForeignKey('product.id'))
    Quantity = db.Column(db.Integer)
    shipped_in__at = db.Column(db.Date, default=_get_date)
    Cost = db.Column(db.Integer)
    Barcode = db.Column(db.Integer)


@app.route('/<name>/<email>/<password>/<designation>/<price>')
def index(name, email, password, designation, price):
    a = Product(name=name, category=email, description=password, barcode=designation, price = price )
    db.session.add(a)
    db.session.commit()
    return '<h1>Added New User!</h1>'


@app.route('/<name>')
def get_user(name):
    e = Employee.query.filter_by(name=name).first()

    return f'<h1>The name and ID are: {e.name} , {e.id}</h1>'


if __name__ == '__main__':
    app.run()
