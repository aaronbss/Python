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
