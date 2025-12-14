from flask import render_template, redirect, url_for, flash, request, current_app
from flask_sqlalchemy import SQLAlchemy
#from db_file import db, login, login_manager, cache
#from models import TUser, TUserRoles, TRole
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_caching import Cache
#from auth import auth_bp
from . import auth
from ..database import db
from ..extensions import cache
from .models import TUser, TUserRoles, TRole
from .forms import RegistrationForm, LoginForm

@auth.route('/auth')
@login_required
def test():
    return render_template('test.html')
"""


import os
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
"""
"""
from . import auth_bp

"""
#from werkzeug.security import generate_password_hash, check_password_hash
@auth.route('/dashboard')
#@login_required
def dashboard():
    return render_template('dashboard.html')

# Cache Test Route
@auth.route('/cache_test')
#@login_required
def cache_test():
    # Example of how to work with cache

    cache.set("commune", current_user.username)
    cached_data = cache.get("commune")

    return render_template('cache_test.html', data=cached_data)


# Registration Route
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Correct the hashing method to pbkdf2:sha256
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        new_user = TUser(username=username, password=hashed_password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('User created successfully!', 'success')
            return redirect(url_for('auth.login'))
        except:
            db.session.rollback()
            flash('Error creating user!', 'danger')
    
    return render_template('register.html')

# Login Route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = TUser.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            # Ensure correct redirect
            #return redirect(url_for('auth.dashboard'))  # Ensure the 'auth.dashboard' endpoint is correct
            #return redirect(url_for('parsel.parsel'))
            return redirect(url_for('dossier.dossier'))
        else:
            flash('Invalid username or password!', 'danger')

    return render_template('login.html')
    
from flask_login import logout_user, login_required
from flask import redirect, url_for, flash

# Logout Route
@auth.route('/logout')
@login_required
def logout():
    logout_user()  # Logs the user out
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))  # Redirects to the login page

