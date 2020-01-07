from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register!')

    def check_email(self, field):
        # Check if not None for that user email!
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def check_username(self, field):
        # Check if not None for that username!
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry, that username is taken!')

class AddForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    category = StringField('category', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    barcode = StringField('barcode', validators=[DataRequired()])
    price = IntegerField('price', validators=[DataRequired()])
    quantity = IntegerField('quantity', validators=[DataRequired()])
    submit = SubmitField('Add New Product!')

    def add_products(self,field):
        if product.query.filter_by(barcode=field.data).first():
            raise ValidationError('barcode has been registered already!')

class delform(FlaskForm):
    barcode=StringField('Barcode of the product that has to be removed',validators=[DataRequired()])
    submit = SubmitField('Deleted the product')


class updateform(FlaskForm):
    barcode=StringField('Barcode of the product that has to be updated',validators=[DataRequired()])
    quantity = IntegerField('Set Quantity ', validators=[DataRequired()])
    submit = SubmitField('Update the product')

class searchform(FlaskForm):
    barcode=StringField('Enter barcode to search')
    name = StringField('Enter name of the product to be searched ')
    category = StringField('Enter category of the product to be searched ')
    submit = SubmitField('Search the product')


class sellform(FlaskForm):
    barcode=StringField('Barcode of the product that has to be sold',validators=[DataRequired()])
    quantity = IntegerField('Quantity to buy ', validators=[DataRequired()])
    submit = SubmitField('SELL')
