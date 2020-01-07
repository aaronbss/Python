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
    data1=db.engine.execute("select category from product")
    names1 = [row[0] for row in data1]
    data2=db.engine.execute("select barcode from product")
    names2 = [row[0] for row in data2]
    data3=db.engine.execute("select price from product")
    names3 = [row[0] for row in data3]
    data4=db.engine.execute("select quantity from product")
    names4 = [row[0] for row in data4]
    return render_template('products.html',names=names,names1=names1,names3=names3,names2=names2,names4=names4)

@app.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    form = updateform()

    if form.validate_on_submit():
        #Barcode = products(barcode=form.barcode.data)
        Barcode=form.barcode.data
        Quantity=form.quantity.data
        print(type(Barcode))
        #Barcode=str(Barcode)
        data=db.engine.execute("update product set quantity=? where barcode=?",Quantity,Barcode)
        db.session.commit()
        flash('The product has been Updated successfully')
        return redirect(url_for('welcome_user'))
    return render_template('update.html',form=form)


@app.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    form = delform()

    if form.validate_on_submit():
        #Barcode = products(barcode=form.barcode.data)
        Barcode=form.barcode.data
        #Barcode=str(Barcode)
        print(Barcode)
        data=db.engine.execute("delete from product where barcode=?",Barcode)
        #sql = "delete from product where barcode='%s'"
        #data=db.engine.execute(sql,Barcode)
        db.session.commit()
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()


        if user.check_password(form.password.data) and user is not None:
            #Log in the user

            login_user(user)
            flash('Logged in successfully bro.')
            next = request.args.get('next')

            # So let's now check if that next exists or no, otherwise it'll go to
            # the welcome page.
            if next == None or not next[0]=='/':
                next = url_for('welcome_user')

            return redirect(next)
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
