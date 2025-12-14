from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, session
parsel = Blueprint('parsel', __name__)
from . import parsel
#from . import routes
#from jinja2 import Environment
from flask_caching import Cache
import os
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
#from . import parsel_bp
#parsel_bp = Blueprint('parsel', __name__, template_folder='/templates/parsel')
from .forms import Form
from .queries import fetch_dossiers_by_no_interne, fetch_dossiers_by_id, get_parcelle_by_idsuf, get_all_t_demande, get_all_parcelles, get_all_parceldem, get_all_t_com2023, fetch_sections_by_commune
#def fetch_dossiers_by_no_interne(no_interne), def fetch_dossiers_by_id(user_id), def fetch_orders_by_id(user_id), def fetch_orders_by_order_id(order_id), def get_parcelle_by_idsuf(idsuf), def get_all_t_demande(), def get_all_parcelles(),def get_all_parceldem(), def get_all_t_com2023(), def fetch_sections_by_commune(idcom)
from .methods import total_balance, header
from ..database import db
from ..extensions import cache
#from .models import TParceldem, TCom2023, TCadastre

@parsel.route('/bof')
#@login_required
def zut():
    return render_template('templates/test.html')
"""
Module docstring: This module provides functionality
for Cellmart wesite developed using flask.
"""
from flask import render_template, redirect, url_for, flash, request, current_app
from flask_sqlalchemy import SQLAlchemy

#from db_file import db, login, login_manager, cache

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

#from parsel import parsel_bp
#, db, login_manager, cache


import os
"""
from flask import Flask, Blueprint, render_template

templates = os.path.join(os.path.dirname(__file__), 'templates')

parsel_bp = Blueprint('parsel', __name__, template_folder='templates', static_folder='static')
"""
import sys
import platform
import flask
import re
import logging
import os
#from app import db
#from auth.forms import LoginForm, RegistrationForm
#from models import TUser
from flask import render_template, redirect, url_for, flash, request 
from flask_login import current_user, login_user, logout_user 
import sqlalchemy as sa 
from urllib.parse import urlsplit
from flask import render_template
from flask_login import login_required
#from forms import *
#from forms import UserForm

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

#from db_init import db
from docxtpl import DocxTemplate
from flask import Response
from io import BytesIO
from flask import Flask, send_file

from datetime import datetime
from flask import Flask, request, redirect, url_for, session, flash
from flask import render_template
#from db_init import create_app
#from db_init import db
#from model import UserDetails, Product, OrderDetails, TCadastre, TParceldem, TCom2023, TCadastre, TPub, TUsager, TDemande, Country, City, Customer
#from app import db
#from models import TUser
#from parsel import parsel_bp

from sqlalchemy.sql import text
from sqlalchemy import desc, asc, and_, select, text
#from model import Base

import flask
import flask_login
from flask import Blueprint
from flask_login import LoginManager
from flask import Flask, render_template
from flask_htmx import HTMX
#Base = db.session.query

# Create the logger
logger = logging.getLogger('failed_login_attempts')
logger.setLevel(logging.INFO)

# Create a file handler
handler = logging.FileHandler('failed_login_attempts.log')
logger.addHandler(handler)
'''
app = create_app(os.getenv("CONFIG_MODE"))
app.secret_key = '12345678'
'''
#from database import db
from flask import render_template
#from flask.blueprints import Blueprint
#from parsel import parsel_bp

"""
parsel = Blueprint('parsel_bp', __name__,
                 template_folder='../templates',
                 static_folder='../static')
"""                
   
#from database import db
from flask import Flask
import os.path


from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, func, cast, Float 
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import relationship,scoped_session,sessionmaker,aliased

from flask import Flask, render_template, request, jsonify, json
from flask_sqlalchemy import SQLAlchemy  
from wtforms import SelectField
from flask_wtf import FlaskForm

from flask import session
    

from werkzeug.debug import DebuggedApplication
   
from flask_caching import Cache
import time

#cache = Cache(app)

@parsel.route('/pay', methods=["POST","GET"])
def pay():    
    t_parceldem = get_all_parceldem()
    #t_parceldem = db.session.query(TParceldem).filter(TParceldem.par_nointerne.like("C22160001")).all()
    cache.set("commune", str("Sélectionner une commune"))    
    if request.method == 'POST':
        commune = cache.get("commune")
        section = cache.get("section")
        parcelles = cache.get("parcelles")
        form = Form()
        '''
        commune = db.session.query(TCom2023).filter_by(com=form.commune.data).first()
        cache.set("commune", db.session.query(TCom2023).filter_by(com=form.commune.data).first())
        section = db.session.query(TCadastre).filter_by(ccosec=form.section.data).first()
        cache.set("section", db.session.query(TCadastre).filter_by(ccosec=form.section.data).first())
        #parcelles = db.session.query(TCadastre.idsuf).where(and_((TCadastre.idcom==format(commune.com),(TCadastre.ccosec==format(section.ccosec))))).all()
        parcelles = db.session.query(TCadastre.idsuf).where(and_((TCadastre.idcom==commune.com),(TCadastre.ccosec==section.ccosec))).all()
        cache.set("parcelles", db.session.query(TCadastre.idsuf).where(and_((TCadastre.idcom==commune.com),(TCadastre.ccosec==section.ccosec))).all())
        '''
        #form.commune.choices = [(commune.com, commune.libelle) for commune in db.session.query(TCom2023).filter_by(dep='22').all()]
        form.commune.choices = [("", "Sélectionner une commune")]+[(commune.com, commune.libelle) for commune in db.session.query(TCom2023).filter_by(dep='22').all()]
            
        t_com2023 = get_all_t_com2023()
        #parcelles = get_all_parcelles()
        #com='search_com2023_id'
        #sections = fetch_sections_by_commune('22278')
   
        fv = flask.__version__
        pv = platform.python_version()
        # check whether user is logged or not
    
        # Get the order details from the form
        #user_id = session['user']['id']
        par_idsuf = request.form.get('parcelle_idsuf')
        #quantity = int(request.form.get('quantity'))
        #product = get_product_by_id(product_id)
        #parcelle = get_parcelle_by_idsuf(idsuf)
        #price = float(product.price)
        #total = price * quantity
        no_interne = str(session.get('no_interne'))
        #par_surface = str('1')
        #user = session.query(User.name).filter(User.id == 1).first()
        #par_surface = session.query(TCadastre.dcntsf).filter(TCadastre.idsuf == par_idsuf).first()
        #user = User.query.filter_by(username=username).first()
        #par_surface = db.session.query(TCadastre.dcntsf).filter(TCadastre.idsuf == par_idsuf).first()
        import re        
        par_surface = re.sub(r'\D', '', str(db.session.query(TCadastre.dcntsf).filter(TCadastre.idsuf == par_idsuf).first()))
        #par_surface = re.sub(r'\D', '', str(par_surface))
        print('par_surface:', par_surface)
        # Save the order details to the DB
        t_parceldem = TParceldem(par_idsuf=par_idsuf,
                                     par_nointerne=no_interne, par_surface=par_surface)
        
    newpar = db.session.query(TParceldem).filter(and_(TParceldem.par_idsuf == par_idsuf, TParceldem.par_nointerne == no_interne)).first()

    if newpar is not None:
        #flash('Parcelle {par_idsuf} déja sélectionnée.')
        #return 'hello'        
        #return flash('La parcelle : %s, a déjà été demandée dans le dossier : %s' % (par_idsuf, "C22160001"))
        message = "Attention : cette parcelle " + str(par_idsuf) + " a déjà été sélectionnée. Merci d'en sélectionner une autre."  # Concatenation
        flash(message, 'danger')
        return render_template("index.html", t_parceldem=get_all_parceldem(),
        parcelles=parcelles, form=form, pv=pv, fv=fv,
        username=current_user.username)  # return index.html with username of logged user

    else:
        #return 'hello'

        db.session.add(t_parceldem)
        db.session.commit()
        #print(t_parceldem)
        #return redirect(url_for('parsel.home'))
        
        no_interne = str(session.get('no_interne'))
        bal = db.session.query(text("""sum(cast(par_surface as int)) FROM t_parceldem where par_nointerne=:numdoss""")).params(numdoss=no_interne).all()

        import re

        balance = re.sub(r'\D', '', str(bal))

        num_str = int(str(balance)) / 10000
        print('num_str :', num_str)
  
        balance = f"{str(num_str).replace('.', ',')} ha"        
        
        return render_template("index.html", balance=balance, t_parceldem=get_all_parceldem(),
        parcelles=parcelles, form=form, pv=pv, fv=fv,
        username=current_user.username)  # return index.html with username of logged user


@parsel.route('/test', methods=['GET', 'POST'])
#@login_required
#@current_app.cache.cached(timeout=60)  # Cache the view for 60 seconds
def test():
    # Explicitly push the app context
    #with app.app_context():
    # Simulating some dynamic data
    dynamic_data = "This is a dynamically generated value that will be cached."
    return render_template('test.html', dynamic_data=dynamic_data)
    
        
#insert data to mysql database via html forms
@parsel.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        '''
        t_parceldem = get_all_parceldem()
        order_details = get_all_order_details()
        products = get_all_products()
        t_com2023 = get_all_t_com2023()
        parcelles = get_all_parcelles()
        all_data = db.session.query(TCadastre).filter(TCadastre.idsuf.like('220010000A%')).all() 
        form = Form()   
        fv = flask.__version__
        pv = platform.python_version()
        name = session['user']['name']
        userId = session['user']['id']
        '''
        idsuf = request.form['idsuf']
        ccosec = request.form['ccosec']
        dcntsf = request.form['dcntsf']
        idcom = request.form['idcom']        
        
        my_data = TCadastre(idsuf=idsuf, ccosec=ccosec, dcntsf=dcntsf, idcom=idcom)
        
        newidsuf = db.session.query(TCadastre).filter(TCadastre.idsuf == idsuf).first()

    if newidsuf is not None:
        #flash('Parcelle {par_idsuf} déja sélectionnée.')
        #return 'hello'        
        #return flash('La parcelle : %s, a déjà été demandée dans le dossier : %s' % (par_idsuf, "C22160001"))
        message = "Attention : cette parcelle " + str(idsuf) + " existe déjà dans le cadastre. Merci de vérifier vos références cadastrales."  # Concatenation
        flash(message, 'error_message')
        #return render_template("index.html", t_parceldem=get_all_parceldem(), parcelles=parcelles, form=form, pv=pv, fv=fv, username=session[
        #'user']['name'], order_details=order_details, products=products)  # return index.html with username of logged user
        return redirect(url_for('parsel.parsel'))
    else:
        #return 'hello'
    
        db.session.add(my_data)
        db.session.commit()
  
        flash("Nouvelle parcelle ajoutée avec succès dans le cadastre. \
        Merci de bien vouloir la sélectionner.")
        return redirect(url_for('parsel.parsel'))
  
#update employee
@parsel.route('/update', methods = ['GET', 'POST'])
@cache.cached(timeout=0)
def update():
    if request.method == 'POST':
        my_data = TCadastre.query.get(request.form.get('idt_cadastre'))
  
        my_data.idsuf = request.form['idsuf']

  
        db.session.commit()
        flash("Employee Updated Successfully")
        return redirect(url_for('parsel.Index'))
  
#delete employee
@parsel.route('/delete/<idt_cadastre>/', methods = ['GET', 'POST'])
def delete(idt_cadastre):
    my_data = TCadastre.query.get(idt_parceldem)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully")
    return redirect(url_for('parsel.Index'))


class Form(FlaskForm):

    commune = SelectField('commune', choices=[])
    section = SelectField('section', choices=[])
    parcelle = SelectField('parcelle', choices=[])  

@parsel.route('/section/<get_section>', methods=['GET', 'POST'])
#@parsel_bp.route('/section')
#@login_required
def sectionbycommune(get_section):
    #section = TCadastre.query.distinct(TCadastre.ccosec).filter_by(idcom=get_section).all()
    section = db.session.query(TCadastre).distinct(TCadastre.ccosec).filter_by(idcom=get_section).all()
    #form.commune.default = [('0', '-- select an option --')] + section
    sectionArray = []
    for parcelle in section:
        sectionObj = {}
        sectionObj['ccosec'] = parcelle.ccosec
        sectionObj['idsuf'] = parcelle.idsuf
        sectionObj['idcom'] = parcelle.idcom
        sectionArray.append(sectionObj)
    return jsonify({'sectioncommune' : sectionArray})
"""  
@parsel_bp.route('/parcelle/<get_parcelle>', methods=['GET', 'POST'])
#@parsel_bp.route('/parcelle')
#@login_required
def parcelle(get_parcelle):
    section_data = db.session.query(TCadastre).filter_by(ccosec=get_section).all()
    parcelleArray = []
    for parcelle in section_data:
        parcelleObj = {}
        parcelleObj['ccosec'] = parcelle.ccosec
        parcelleObj['idsuf'] = parcelle.idsuf        
        parcelleObj['idcom'] = parcelle.idcom
        parcelleArray.append(parcelleObj)
    return jsonify({'parcellelist' : parcelleArray}) 

# Define a cache decorator
def cache_decorator(timeout=5 * 60, key_prefix='view/%s'):
    def decorator(f):
        def decorated_function(*args, **kwargs):
            cache_key = key_prefix % request.path
            cached_response = cache.get(cache_key)
            if cached_response:
                return cached_response
            response = f(*args, **kwargs)
            cache.set(cache_key, response, timeout=timeout)
            return response
        return decorated_function
    return decorator
"""
@parsel.route('/parsel', methods=['GET', 'POST'])
@parsel.route('/parsel')
@login_required
#@current_app.cache.cached(timeout=0)  # Cache the view for 60 seconds
#@cache.cached(timeout=0)
#@cache_decorator(timeout=60)
def parsel():
#@parsel_bp.route('/',methods=["POST","GET"])
# ‘/’ URL is bound with home() function.
#def home():   
    t_parceldem = get_all_parceldem()
    #balance = total_balance()
    #print(balance)
    #print('balance:', str(balance))
    t_com2023 = get_all_t_com2023()
    parcelles = get_all_parcelles()
    all_data = db.session.query(TCadastre).filter(TCadastre.idsuf.like('220010000A%')).all() 
    form = Form()
    #balance = db.session.query(sum(int(str(TParceldem.par_surface)))).filter(TParceldem.par_nointerne.like(no_interne)).first()
    no_interne = str(session.get('no_interne'))
    bal = db.session.query(text("""sum(cast(par_surface as int)) FROM t_parceldem where par_nointerne=:numdoss""")).params(numdoss=no_interne).all()
    #bal = db.session.query(text("""sum(cast(par_surface as real)) FROM t_parceldem where par_nointerne=:numdoss""")).params(numdoss=no_interne).all()
    #bal = db.session.query(text("""sum(cast(replace(substr(par_surface, -2), ',', '.') as double precision)) FROM t_parceldem where par_nointerne=:numdoss""")).params(numdoss=no_interne).all()
    #bal = db.session.query(text("""sum(cast(replace(trim(trailing '0' from par_surface::text), ',', '.') as int) FROM t_parceldem where par_nointerne=:numdoss""")).params(numdoss=no_interne).all()
    #bal = db.session.query(text("""sum(cast(trim(trailing '0' from replace(par_surface, ',', '')::text) as int)) FROM t_parceldem where par_nointerne=:numdoss""")).params(numdoss=no_interne).all()
    #trim(trailing '0' from atomic_mass::text)::numeric
    print('bal1:', bal)

    if bal == '[(None,)]':
        bal == '[(1,)]'
        print('bal2:', bal)
        import re
        balance = re.sub(r'\D', '', str(bal))
        num_str = int(str(balance)) / 10000
        print('num_str :', num_str)
        balance = re.sub(r'\D', '', str(bal))
        num_str = int(str(balance)) / 10000
        balance = f"{str(num_str).replace('.', ',')} ha" 
    import re    
    balance = re.sub(r'\D', '', str(bal))
    #number = request.form.get('number')
    if balance and balance.isdigit():
        #return f'You entered: {balance}'
        num_str = int(str(balance)) / 10000   
        balance = f"{str(num_str).replace('.', ',')} ha" 
        print('balance:', balance)
    """
    else:
        return 'Invalid input, please enter a number', 400    
    """
    fv = flask.__version__
    pv = platform.python_version()
    # check whether user is logged or not
    
    form = Form()
    form.commune.choices = [("", "Sélectionner une commune")]+[(commune.com, commune.libelle) for commune in db.session.query(TCom2023).filter_by(dep='22').all()]
         
    if current_user.is_authenticated:
       
        if request.method == 'POST':

            cache.set("section", str(""), timeout=0)
            cache.set("parcelles", str(""), timeout=0)
            commune = db.session.query(TCom2023).filter_by(com=form.commune.data).first()
            cache.set("commune", db.session.query(TCom2023).filter_by(com=form.commune.data).first())
            section = db.session.query(TCadastre).filter_by(ccosec=form.section.data).first()
            cache.set("section", db.session.query(TCadastre).filter_by(ccosec=form.section.data).first())
            parcelles = db.session.query(TCadastre.idsuf).where(and_((TCadastre.idcom==commune.com),(TCadastre.ccosec==section.ccosec))).order_by(asc(TCadastre.idsuf)).all()
            cache.set("parcelles", db.session.query(TCadastre.idsuf).where(and_((TCadastre.idcom==commune.com),(TCadastre.ccosec==section.ccosec))).order_by(asc(TCadastre.idsuf)).all())
        user = current_user.username
        no_interne = session.get('no_interne')
        flash(no_interne)
        return render_template('index.html', balance=balance, t_parceldem=t_parceldem, parcelles=parcelles, form=form, t_cadastre = all_data, pv=pv, fv=fv, username=user)  # return index.html with username of logged user

    return redirect(url_for('parsel.login'))
    
#total balance calculation
#@parsel_bp.route("/balance")
def total_balance():
    #a = ['1', '2', '3']
    #t_parceldem = get_all_parceldem()
    """
    balance = 0
    #for i in a:
    for TParceldem.par_surface in t_parceldem:
        balance = balance + int(str(TParceldem.par_surface),2)
    """ 
    """
    balance = 0
    for TParceldem in t_parceldem:
        balance = balance + int(TParceldem['par_surface'])
    """    
    #t_parceldem = get_all_parceldem()
    #balance=sum(list.append(int([t_parceldem['par_surface'] for TParceldem in t_parceldem])))
    #balance=sum(int([int(t_parceldem['par_surface']) for t_parceldem in t_parceldem]))
    #balance=sum([t_parceldem.par_surface for TParceldem in TParceldem])
    #return f"Total Balance: {balance}"
    #return jsonify({'sum': balance})
    #balance=sum(int([int(t_parceldem[8]) for TParceldem in t_parceldem]))
    #return f"Total Balance: {balance}"
    
    #no_interne = cache.get("no_interne")
    #no_interne = str(session.get('no_interne'))
    #par_surface = str(TParceldem.par_surface)
    #par_surface = int([TParceldem.par_surface).strip())
    #return db.session.query(TParceldem).filter(TParceldem.par_nointerne.like(no_interne)).all()
    #sections = db.session.query(TCadastre.ccosec.distinct()).where(TCadastre.idcom=='22278').all()
    #parcelles = db.session.query(TCadastre.idsuf).where(and_((TCadastre.idcom==commune.com),(TCadastre.ccosec==section.ccosec))).all()
    no_interne = str(session.get('no_interne'))
    #balance = db.session.query(sum(int(str(TParceldem.par_surface)))).filter(TParceldem.par_nointerne.like(no_interne)).all()
    #return f"Total Balance: {balance}"
    return db.session.query(sum(int(str(TParceldem.par_surface)))).filter(TParceldem.par_nointerne.like(no_interne)).all()


# this method authenticate user with username and password
def authenticate_user(email, password):
    """
    Authenticates user with email & password.

    This method chec if the provided email and password match any users
    credentials stored in DB

    Args:
        email (str):  email to authenticate.
        password (str): password to authenticate.

    Returns:
       user:  if the email and password match, ifnot otherwise.
    """

    # Retrieve the user details based on the provided email
    user = UserDetails.query.filter_by(email=email).first()

    # Check if a user with the provided email exists and if the password matches
    if user and user.check_password(password):
        return {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role
        }
    else:
        return None


def header():
    #pv = print(sys.version)
    #pv = print(platform.python_version())
    fv = flask.__version__
    pv = platform.python_version()
    return render_template('header.html', fv=fv, pv=pv)  # return index.html with username of logged user


"""
@parsel.route('/refresh_field')
def refresh_field():
    # Simulate getting updated data (e.g., from a database)
    updated_data = "Updated content at the time of the request"
    return jsonify({'updated_field': updated_data})
"""    

