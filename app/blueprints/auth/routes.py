from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.models import User, Unit
from app.extensions import db, login_manager

auth_bp = Blueprint('auth_bp', __name__, template_folder='templates')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        unit_name = request.form['unit']

        unit = Unit.query.filter_by(name=unit_name).first()
        if not unit:
            unit = Unit(name=unit_name)
            db.session.add(unit)
            db.session.commit()

        user = User(username=username, role=role, unit=unit)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Compte créé ! Connectez-vous.')
        return redirect(url_for('auth_bp.login'))
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            if user.role == 'manager':
                return redirect(url_for('unit_bp.unit_dashboard'))
            else:
                return redirect(url_for('agent_bp.dashboard'))
        else:
            flash('Identifiants incorrects')
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_bp.login'))
