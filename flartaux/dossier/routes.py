"""
from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from config import Config
from models import db
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
#from models import db, TDemande
#from ..extensions import db, TDemande

#from extensions import db
#from app import db
#from models import db
from models import db, TParceldem, TDemande, Users, TUsager   # importer le modèle
#from extensions import db     # importer la même instance db

from flask import Blueprint, render_template
#dossier = Blueprint('dossier_blueprint', __name__)

# Create the Blueprint instance
#dossier_blueprint = Blueprint('dossier_blueprint', __name__)
dossier = Blueprint('dossier', __name__)
from . import dossier
from sqlalchemy import text
# Import routes to connect with the Blueprint
#from . import routes

"""
import os
print(os.getcwd())
print(app.jinja_loader.searchpath)
"""

@dossier.route('/bof')
def mince():
    return render_template('dossier.html')

import os
from flask import render_template, redirect, url_for, flash

from .forms import Form
#from .models import TDemande 
#from ..auth.models import TUser
from .queries import get_dossier
from .methods import insertdoss
#from ..database import db
#from ..extensions import cache

from flask import render_template, redirect, url_for, flash, request, current_app
from flask_sqlalchemy import SQLAlchemy
#from db_file import db, login, login_manager, cache
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_caching import Cache
#from dossier import dossier_bp

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
#import sqlalchemy as sa 
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
#from .models import TDemande
#TCadastre, TParceldem, TCom2023, TCadastre, 
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

from flask import render_template
from flask.blueprints import Blueprint
#from parsel import parsel_bp

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
"""    
def setup_database(app):
    with app.app_context():
        db.create_all()
"""
from werkzeug.debug import DebuggedApplication
 
from flask_caching import Cache
import time

import sys
import platform
import flask
import re
import logging
import os
from datetime import datetime

#from database import db
from flask import Flask, request, redirect, url_for, session, flash
from flask import render_template
from flask.blueprints import Blueprint
from flask import current_app
from flask import Flask, session
from flask import request, flash

#from model import Base
import bcrypt

import os

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.inspection import inspect
from sqlalchemy.dialects import postgresql
#from sqlalchemy import db.db.db.mapped_column, Table, Column, Bigdb.Integer, db.Integer, db.db.Text, db.Date, db.Boolean, db.db.db.String, ForeignKey
from sqlalchemy import desc
from flask_wtf import FlaskForm
from wtforms import StringField
#from flask_autodoc import Autodoc
#from flask_caching import Cache

#cache = Cache()

#from .cache import cache

#from ..zut.models import TParceldem

#@dossier_blueprint.route('/getdossier', methods=['GET', 'POST'])
@dossier.route('/getdossier', methods=['GET', 'POST'])
def getdossier():

    dossiers = get_dossier()
    if request.method == 'POST' :
        username=current_user.username
        user_id = current_user.id
        no_interne = str(request.form.get('no_interne'))
        no_pacage_demandeur = str(request.form.get('no_pacage_demandeur'))
        u_nom_raison_sociale = str(request.form.get('u_nom_raison_sociale'))
        session['no_interne'] = no_interne
        dossier_cible = session.get('no_interne')
        # Étape 1 : Récupérer les parcelles du dossier courant
        parcelles_courantes = db.session.query(TParceldem.par_idsuf) \
            .filter(TParceldem.par_nointerne == dossier_cible) \
            .distinct().all()
        idsuf_list = [p[0] for p in parcelles_courantes]

        # Étape 2 : Vérifier si chaque parcelle apparaît dans au moins un autre dossier
        parcelles_partagees = db.session.query(
            TParceldem.par_idsuf
        ).filter(
            TParceldem.par_idsuf.in_(idsuf_list),
            TParceldem.par_nointerne != dossier_cible
        ).distinct().all()

        # Étape 3 : Le nombre total de parcelles partagées
        nb_partagees = len(parcelles_partagees)
        
        #cache.set("current_no_interne", no_interne)
        #cache.add("current_no_interne", no_interne)
        
        no_interne = fetch_dossiers_by_no_interne(no_interne)

        fv = flask.__version__
        pv = platform.python_version()
        return render_template('dossier.html', fv=fv, pv=pv,
        dossiers=no_interne, no_pacage_demandeur=no_pacage_demandeur, u_nom_raison_sociale=u_nom_raison_sociale, username=username, user_id=user_id, nb_partagees=nb_partagees)

        db.session.commit()

    return redirect(url_for('dossier.dossier'))
    
@dossier.route('/insertdoss', methods=['POST'])
def insertdoss():
    if request.method == 'POST':
        no_interne = request.form['no_interne']
        date_complet = datetime.today().strftime('%d-%m-%y')
        user_id = request.form['user_id']
        
        # 🔧 Réaligner la séquence après l'insertion
        # Remplace bien par le nom exact de ta séquence et table
        seq_name = 'w_sadr_artaux.t_demande_idt_demande_seq'
        table_name = 'w_sadr_artaux.t_demande'

        db.session.execute(
            text(f"SELECT setval('{seq_name}', (SELECT COALESCE(MAX(idt_demande), 1) FROM {table_name}) + 1, false)")
        )
        db.session.commit()
        
        my_data = TDemande(
            no_interne=no_interne,
            date_complet=date_complet,
            user_id=user_id
        )

        db.session.add(my_data)
        db.session.commit()



        flash("Nouveau dossier ajouté avec succès !")
        return redirect(url_for('dossier.dossier'))

 
class Form(FlaskForm):
    no_interne = StringField('no_interne')

@dossier.route('/dossier')
#@login_required
# ‘/’ URL is bound with orders() function.
def dossier():
    # check whether user is logged or not
    #if 'user' in session:
    if current_user.is_authenticated:
        # if user has a active session get the username from the session
        name = current_user.username
        userId = str(current_user.id)
        user_dossiers = fetch_dossiers_by_id(userId)
        fv = flask.__version__
        pv = platform.python_version()
        #get_newnointerne = TDemande.query.filter_by(user_id=userId).order_by(desc(TDemande.no_interne)).first()
        #get_newnointerne = db.session.query(TDemande).filter_by(user_id=userId).order_by(desc(TDemande.no_interne)).first()
        #form = Form()
        string = str(str(TDemande.query.with_entities(TDemande.no_interne).order_by(TDemande.no_interne.desc()).first())[7:11])
        cleaned_value = string.replace("',", "")
        newnointerne = str(f"{int(cleaned_value)+1:04d}")
        x = len(newnointerne)
        date = datetime.now().strftime("%y/%m/%d")
        if x == 3:
            get_newnointerne = str(str('C22')+str(date[0:2])+str('0')+str(newnointerne))
            get_user_id = current_user.id
            return render_template('dossier.html', fv=fv, pv=pv,
            username=current_user.username, dossiers=user_dossiers, get_user_id=get_user_id, get_newnointerne=get_newnointerne)
            flash(date[0:2])
            flash(str(newnointerne))
            flash(x)
        #date.strftime("%d/%m/%y")
        get_newnointerne = str(str('C22')+str(date[0:2])+str(newnointerne))
        #get_user_id = session['user']['id']
        get_user_id = current_user.id
        flash(date[0:2])
        flash('test :' , str(newnointerne))
        flash(x)
        #form.no_interne.data = get_newnointerne
        #form = StringField('no_interne', default='{{get_newnointerne}}')
        return render_template('dossier.html', fv=fv, pv=pv,
        username=current_user.username, dossiers=user_dossiers, get_user_id=get_user_id, get_newnointerne=get_newnointerne)
    # return login page to the user if user does not have an active session
    return redirect(url_for('auth.login'))

def fetch_dossiers_by_id(user_id):

    dossiers = TDemande.query.filter_by(user_id=user_id).order_by(desc(TDemande.no_interne)).all()

    dossiers_list = []
    for dossier in dossiers:
        dossiers_list.append({
            'no_interne': dossier.no_interne,
            'date_de_depot': dossier.date_de_depot
        })

    return dossiers_list
  
def fetch_dossiers_by_no_interne(no_interne):
    '''
    dossiers = db.session.query(TDemande
        ).filter(TDemande.no_interne == no_interne
        ).with_entities(TDemande.no_interne, TDemande.date_de_depot 
        ).all()
    '''
    dossiers = db.session.query(TDemande, TUsager
        ).filter(TDemande.no_interne == no_interne
        ).join(TUsager, TUsager.u_pacage == TDemande.no_pacage_demandeur
        ).with_entities(TDemande.no_interne, TDemande.date_de_depot,\
        TDemande.no_pacage_demandeur, TUsager.u_nom_raison_sociale 
        ).all()
    dossiers_list = []
    for dossier in dossiers:
        dossiers_list.append({
            'no_interne': dossier.no_interne,
            'date_de_depot': dossier.date_de_depot,
            'no_pacage_demandeur': dossier.no_pacage_demandeur,          
            'u_nom_raison_sociale': dossier.u_nom_raison_sociale,
        })

    return dossiers_list

def get_dossier():
    #if 'user' in session:
    if current_user.is_authenticated:
        #user_id = current_user.id
        #username=current_user.username
        user_id = current_user.id
        no_interne = str(request.form.get('no_interne'))
        #cache.set("current_no_interne", no_interne)
        flash('test :' , str(no_interne))
        print('order_id:', str(no_interne))
        return db.session.query(TDemande).where(TDemande.no_interne == str(no_interne))
    return db.session.query(TDemande).where(TDemande.no_interne == str(no_interne))    
