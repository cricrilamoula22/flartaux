from flask import Blueprint, render_template
#dossier = Blueprint('dossier_blueprint', __name__)

# Create the Blueprint instance
#dossier_blueprint = Blueprint('dossier_blueprint', __name__)
book_list = Blueprint('book_list', __name__)
from . import book_list
# Import routes to connect with the Blueprint
#from . import routes

"""
import os
print(os.getcwd())
print(app.jinja_loader.searchpath)
"""

import os
from flask import render_template, redirect, url_for, flash

#from .forms import Form
#from .models import TDemande 
"""
from ..auth.models import TUser
from .queries import get_dossier
from .methods import insertdoss
"""
from extensions import db
from extensions import cache


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


from flask import Response
from openpyxl import Workbook
#from openpyxl.writer.excel import save_virtual_workbook
import flask_excel as excel


import pandas as pd
import io
from flask import make_response

from flask import Flask, render_template
from flask_htmx import HTMX

@book_list.route('/book_list')
def book_list():
    #books = Book.objects.all()
    #param = '%%jd%%'
    #books = Book.objects.raw("SELECT * FROM book WHERE title LIKE %s", [param])
    #books = Book.objects.raw("SELECT * FROM book WHERE title LIKE '%%i%%'")
   
    param = '%%%%%'
    param_date_pub_pref = '20240320'
    param_date_complet_1 = '20240307'
    param_date_complet_2 = '20240320'
    param_ccodro = 'P'
    param_com_in_1 = '22046'
    param_com_in_2 = '22050'
    param_par_idsuf = '222800000C0200'
    

    with db.engine.begin() as conn:
        ResultSet = conn.execute(text("""
SELECT DISTINCT libelle,         
        array_to_string(array_agg(CONCAT(w, z, x, y) order by z asc, x asc, y asc), ' - ') 
        as parcelles,
        REPLACE(TO_CHAR(SUM(CAST(REPLACE( par_surface, ',','.') AS double precision)), '000.9999'), '.',',') as superficie, 
        nomproprietaireoumandataire, idprocpte, adresseproprietaireoumandataire, no_interne 
		   from 
        (SELECT DISTINCT libelle, CONCAT (SUBSTRING(t_parceldem.par_idsuf, 1, 2), SUBSTRING(t_parceldem.par_idsuf, 6, 3)), par_idsuf, par_surface,
        concat(t_parceldem.par_idsuf, ' ') AS u, SUBSTRING ( RIGHT( par_idsuf, 10 ) FROM '[A-Z]+') AS z,
        regexp_replace(SUBSTRING ( RIGHT( par_idsuf, 6 ) FROM '[0-9]+[\\d]+' ), '(^|-)0*', '', 'g')::int as x,
        SUBSTRING( par_idsuf, 6, 3 ) as w, SUBSTRING ( RIGHT( par_idsuf, 6 ) FROM '[A-Z]+$' ) AS y,
        replace(regexp_replace(CONCAT(array_agg(ddenom)),'{|}| |',' ','gi'), ',',CHR(13)) as nomproprietaireoumandataire, idprocpte,
        replace(regexp_replace(CONCAT(array_agg(dlign6)),'{|}| |',' ','gi'), ',',CHR(13)) as adresseproprietaireoumandataire, no_interne
          FROM t_parceldem
          LEFT JOIN t_demande
        ON t_parceldem.par_nointerne = t_demande.no_interne       
          RIGHT JOIN t_com2023
        ON com LIKE CONCAT(SUBSTRING(t_parceldem.par_idsuf, 1, 2), CASE WHEN SUBSTRING(t_parceldem.par_idsuf, 6, 3) LIKE '000' THEN SUBSTRING(t_parceldem.par_idsuf, 3, 3)
           ELSE CONCAT(SUBSTRING(t_parceldem.par_idsuf, 1, 2),SUBSTRING(t_parceldem.par_idsuf, 3, 3)) END)
           AND libelle IN(SELECT libelle FROM t_com2023 
WHERE dep = '22')
           OR com LIKE CONCAT(SUBSTRING(t_parceldem.par_idsuf, 1, 2),SUBSTRING(t_parceldem.par_idsuf, 3, 3)) AND libelle IN(SELECT libelle FROM t_com2023 
WHERE dep = '22')       
          RIGHT JOIN t_usager 
        ON CAST(t_demande.no_pacage_demandeur AS INT) = CAST(t_usager.u_pacage AS INT)
          RIGHT JOIN t_proprietaires
        ON t_parceldem.par_idpropr = t_proprietaires.idprocpte WHERE date_complet BETWEEN '20250101' and '20250331'
        AND no_interne LIKE '%' AND idprocpte LIKE '%' GROUP BY idprocpte, date_complet, par_nointerne, libelle,
        t_demande.no_interne, t_usager.u_pacage, t_usager.u_nom_raison_sociale, t_parceldem.par_idsuf,
        t_parceldem.par_surface ORDER BY nomproprietaireoumandataire asc, no_interne DESC) as bof 
        GROUP BY bof.libelle, bof.no_interne, bof.nomproprietaireoumandataire, bof.idprocpte, bof.adresseproprietaireoumandataire 
		  ORDER BY libelle ASC, parcelles ASC, bof.no_interne DESC        
        """))

        books = ResultSet.fetchall()
        for row in books:
            print("%s, %s" % (row[0], row[1]))
            
    return render_template('book_list.html', books=books)
