from myproject import app,db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, redirect, request, url_for, flash,abort
from flask_login import login_user,login_required,logout_user
from myproject.models import User,products
from myproject.forms import LoginForm, RegistrationForm,AddForm,delform,updateform,searchform,sellform
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import sessionmaker,relationship

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
    data1=db.engine.execute("select category from product order by id")
    names1 = [row[0] for row in data1]
    data2=db.engine.execute("select barcode from product order by id")
    names2 = [row[0] for row in data2]
    data3=db.engine.execute("select price from product order by id")
    names3 = [row[0] for row in data3]
    data4=db.engine.execute("select quantity from product order by id")
    names4 = [row[0] for row in data4]
    return render_template('products.html',names=names,names1=names1,names3=names3,names2=names2,names4=names4)

@app.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    form = updateform()

    if form.validate_on_submit():
        #Barcode = products(barcode=form.barcode.data)
        Barcode=''
        Barcode=form.barcode.data
        Quantity=form.quantity.data
        print(type(Barcode))
        #Barcode=str(Barcode)
        data=db.engine.execute("update product set quantity=? where barcode=?",Quantity,Barcode)
        db.session.commit()
        flash('The product has been Updated successfully')
        return redirect(url_for('welcome_user'))
    return render_template('update.html',form=form)


@app.route('/sell', methods=['GET', 'POST'])
@login_required
def sell():
    form = sellform()

    if form.validate_on_submit():
        #Barcode = products(barcode=form.barcode.data)
        Barcode=form.barcode.data
        Quantity=form.quantity.data
        data2=db.engine.execute("select quantity from product where barcode=?",Barcode)
        names = [row[0] for row in data2]
        #Barcode=str(Barcode)
        Total=names[0]-Quantity
        data=db.engine.execute("update product set quantity=? where barcode=?",Total,Barcode)
        print(Barcode)
        print(names[0])
        print(Total)
        db.session.commit()
        flash('The product has been Sold successfully')
        return redirect(url_for('sell'))
    return render_template('sell.html',form=form)





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


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = searchform()
    #Barcode = products(barcode=form.barcode.data)
    Barcode=form.barcode.data
    Name=form.name.data
    Category=form.category.data
    if Barcode!='':
        data=db.engine.execute("select name from product where barcode=?",Barcode)
        names = [row[0] for row in data]
        data1=db.engine.execute("select category from product where barcode=?",Barcode)
        names1 = [row[0] for row in data1]
        data2=db.engine.execute("select barcode from product where barcode=?",Barcode)
        names2 = [row[0] for row in data2]
        data3=db.engine.execute("select price from product where barcode=?",Barcode)
        names3 = [row[0] for row in data3]
        data4=db.engine.execute("select quantity from product where barcode=?",Barcode)
        names4 = [row[0] for row in data4]
    elif Name!='':
        data=db.engine.execute("select name from product where name=?",Name)
        names = [row[0] for row in data]
        data1=db.engine.execute("select category from product where name=?",Name)
        names1 = [row[0] for row in data1]
        data2=db.engine.execute("select barcode from product where name=?",Name)
        names2 = [row[0] for row in data2]
        data3=db.engine.execute("select price from product where name=?",Name)
        names3 = [row[0] for row in data3]
        data4=db.engine.execute("select quantity from product where name=?",Name)
        names4 = [row[0] for row in data4]
    elif Category!='':
        data=db.engine.execute("select name from product where category=?",Category)
        names = [row[0] for row in data]
        data1=db.engine.execute("select category from product where category=?",Category)
        names1 = [row[0] for row in data1]
        data2=db.engine.execute("select barcode from product where category=?",Category)
        names2 = [row[0] for row in data2]
        data3=db.engine.execute("select price from product where category=?",Category)
        names3 = [row[0] for row in data3]
        data4=db.engine.execute("select quantity from product where category=?",Category)
        names4 = [row[0] for row in data4]
    else:
        return redirect(url_for('welcome_user'))
    #sql = "delete from product where barcode='%s'"
    #data=db.engine.execute(sql,Barcode)
    flash('Search the product ')
    return render_template('search.html',names=names,names1=names1,names3=names3,names2=names2,names4=names4,form=form)




@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
        form = AddForm()

        if form.validate_on_submit():
            Product = products(name=form.name.data,
                        category=form.category.data,
                        description=form.description.data,
                        barcode=form.barcode.data,
                        price=form.price.data,
                        quantity=form.quantity.data)
            Name=form.name.data
            Category=form.category.data
            Description=form.description.data
            Barcode=form.barcode.data
            Price=form.price.data
            Quantity=form.quantity.data
            data=db.engine.execute("insert into product(name,category,description,barcode,price,quantity) values(?,?,?,?,?,?)",Name,Category,Description,Barcode,Price,Quantity)
            #db.session.add(Product)
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
