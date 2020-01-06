from flask import Flask
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, ForeignKey, select, delete
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
from sqlalchemy.sql import select
import matplotlib.pyplot as plt
import pandas as pd


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.Electronics'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:Anthony10c1997@sneaker.c6x6z62swbhb.eu-west-1.rds.amazonaws.com'
db = SQLAlchemy(app)

engine = create_engine('sqlite:///db.Electronics', echo=True)


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
    __tablename__ = 'orders'
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
    a = Product(name=name, category=email, description=password, barcode=designation, price=price)
    db.session.add(a)
    db.session.commit()
    return '<h1>Added New User!</h1>'


@app.route('/<name>')
def get_user(name):
    e = Product.query.filter_by(name=name).first()

    return f'<h1>The name and ID are: {e.name} , {e.id}</h1>'


@app.route('/')
def test():
    conn = engine.connect()
    s = select([Product])
    data = conn.execute(s)
    for row in data:
        print(row)
    return render_template('test.html', data=data)


@app.route('/100')
def test1():
    conn = engine.connect()
    s = Product.query.filter(Product.barcode == 1234747899).delete()
    #s = Product.delete().where(Product.c.barcode == )
    data = conn.execute(s)
    for row in data:
        print(row)
    return render_template('test.html', data=data)


@app.route('/200')
def chart():
    conn = engine.connect()
    conn.execute('SELECT name, quantity FROM PRODUCTS')


if __name__ == '__main__':
    app.run()
