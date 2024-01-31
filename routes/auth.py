from flask import Blueprint, jsonify, request, session, redirect, url_for, render_template
from flask_login import login_user, logout_user, current_user, login_required, login_manager
from models.user import User
from config.database import db
from passlib.hash import bcrypt

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Check if the username already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400

    # Hash the password
    hashed_password = bcrypt.hash(password)

    # Create a new user with hashed password
    new_user = User(username=username, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'})

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()

    if user and bcrypt.verify(password, user.password_hash):
        login_user(user)
        return jsonify({'message': 'Logged in successfully'})

    return jsonify({'message': 'Invalid username or password'}), 401


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'})


@auth_bp.route('/login1', methods=['GET', 'POST'])
def login1():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.verify(password, user.password_hash):
            login_user(user)
            return redirect(url_for('cart_item.index'))
        else:
            return 'Login Failed. Invalid username or password.'
    return render_template('login.html')


@auth_bp.route('/register1', methods=['GET', 'POST'])
def register1():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            return 'Registration Failed. Username already exists.'

        # Hash the password
        hashed_password = bcrypt.hash(password)

        # Create a new user with hashed password
        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login1'))

    return render_template('register.html')


# Protected route example
@auth_bp.route('/protected')
@login_required
def protected():
    return jsonify({'message': 'This is a protected route'})
