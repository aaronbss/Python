from myproject import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
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

    def __init__(self, email,first_name,last_name, username, password):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password_hash = generate_password_hash(password)

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

    def __init__(self, name,category,description, barcode, price):
        self.name = name
        self.category = category
        self.description = description
        self.barcode = barcode
        self.price = price
