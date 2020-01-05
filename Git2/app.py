from myproject import app,db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, redirect, request, url_for, flash,abort
from flask_login import login_user,login_required,logout_user
#from myproject.models import User,products
from myproject.forms import LoginForm, RegistrationForm,AddForm,delform
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import sessionmaker,relationship

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    # Create a table in the database
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    class products(db.Model, UserMixin):

    __tablename__='product'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    category = db.Column(db.String(64))
    description = db.Column(db.String(128))
    barcode = db.Column(db.String(64), unique=True)
    price = db.Column(db.Integer)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')

@app.route('/products')
@login_required
def product():
    data=db.engine.execute("select name from product")
    names = [row[0] for row in data]
    print(names)
    return render_template('products.html',names=names)

@app.route('/update')
@login_required
def update():
    return render_template('update.html')


@app.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    form = delform()

    if form.validate_on_submit():
        Barcode = products(barcode=form.barcode.data)
        print(Barcode)
        data=db.engine.execute("select name from product")
        names=[row[0] for row in data]
        print(names)
        flash('The product has been deleted')
        return redirect(url_for('welcome_user'))
    return render_template('delete.html',form=form)

@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
        form = AddForm()

        if form.validate_on_submit():
            Product = products(name=form.name.data,
                        category=form.category.data,
                        description=form.description.data,
                        barcode=form.barcode.data,
                        price=form.price.data)
            db.session.add(Product)
            db.session.commit()
            flash('Thanks for adding the new product')
            return redirect(url_for('welcome_user'))
        return render_template('add_product.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out!')
    return redirect(url_for('home'))
