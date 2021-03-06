from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.orm import sessionmaker
from models import *

Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
session = Session()
auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    # if current_user.is_authenticated():
    #     return redirect(url_for('main.index'))
    # else:
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = session.query(User).filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password): 
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    else:
        user.authenticated = True
        session.add(user)
        session.commit()
        login_user(user, remember=remember)
        return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    bio = request.form.get('bio')
    
    # if this returns a user, then the email already exists in database
    user = session.query(User).filter_by(email=email).first()

    # if a user is found, we want to redirect back to signup page so user can try again  
    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=name, bio=bio, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    session.add(new_user)
    session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    user = session.query(User).filter_by(email=current_user.email).first()
    user.authenticated = False
    session.add(user)
    session.commit()
    logout_user()
    return redirect(url_for('main.index'))
