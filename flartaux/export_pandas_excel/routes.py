from flask import Blueprint, render_template
#dossier = Blueprint('dossier_blueprint', __name__)

# Create the Blueprint instance
#dossier_blueprint = Blueprint('dossier_blueprint', __name__)
export_pandas_excel = Blueprint('export_pandas_excel', __name__)
from . import export_pandas_excel
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
from ..database import db
from ..extensions import cache


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
@export_pandas_excel.route('/export_pandas_excel')
def export_pandas_excel():

    # Function is defined somewhere else
    with db.engine.begin() as conn:
        ResultSet = conn.execute(text("select colpivot('_test_pivoted',"
"        'SELECT libelle_commune, par_idsuf, u_nom_raison_sociale, no_interne"
" FROM t_parceldem"
" INNER JOIN t_demande"
" ON t_parceldem.par_nointerne = t_demande.no_interne"
" LEFT JOIN t_commune"
" ON CASE WHEN SUBSTRING(t_parceldem.par_idsuf, 6, 3) LIKE ''000''"
" THEN SUBSTRING(t_parceldem.par_idsuf, 1, 5)"
" ELSE CONCAT (SUBSTRING(t_parceldem.par_idsuf, 1, 2),"
" SUBSTRING(t_parceldem.par_idsuf, 6, 3))"
" END  = t_commune.code_insee_commune "
" INNER JOIN t_usager"
" ON t_demande.no_pacage_demandeur = t_usager.u_pacage"
" WHERE par_idsuf like ''22193000ZH0016%''"
" GROUP BY t_demande.date_complet, t_parceldem.par_idsuf,"
" t_demande.no_interne, t_usager.u_pacage, t_usager.u_nom_raison_sociale,"
" t_commune.libelle_commune, t_parceldem.par_surface"
" ORDER BY par_idsuf asc, no_interne desc,"
" libelle_commune asc LIMIT 100', "
" array['libelle_commune', 'par_idsuf'], array['no_interne', 'u_nom_raison_sociale'],"
" '#.par_idsuf', null);"
" select * from _test_pivoted order by libelle_commune, par_idsuf;"))

        rows = ResultSet.fetchall()
        keys = ResultSet.keys()
        #rows = ResultSet._metadata.keys
        data = rows

   
        # Convert result set to pandas data frame and add columns
        df = pd.DataFrame((tuple(t) for t in data),
            columns=keys)
            #columns=('Date ', 'name', 'username', 'description', 'email','','','','','',''))


        # Creating output and writer (pandas excel writer)
        out = io.BytesIO()
        writer = pd.ExcelWriter(out, engine='xlsxwriter')

   
        # Export data frame to excel
        df.to_excel(excel_writer=writer, header=True, index=True, sheet_name='Sheet1')
        #writer.save()
        writer.close()

   
        # Flask create response 
        r = make_response(out.getvalue())

    
        # Defining correct excel headers
        r.headers["Content-Disposition"] = "attachment; filename=export.xlsx"
        r.headers["Content-type"] = "application/x-xls"

    
        # Finally return response
        return r