from flask import Blueprint, render_template
#dossier = Blueprint('dossier_blueprint', __name__)

# Create the Blueprint instance
#dossier_blueprint = Blueprint('dossier_blueprint', __name__)
test_excel = Blueprint('test_excel', __name__)
from . import test_excel
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
#import flask_excel as excel


import pandas as pd
import io
from flask import make_response

from flask import Flask, render_template
from flask_htmx import HTMX

from flask import Response
from openpyxl import Workbook
#from openpyxl.writer.excel import save_virtual_workbook
#import flask_excel as excel


import pandas as pd
import io
from flask import make_response



import numpy as np
import pandas as pd
from io import BytesIO
from flask import Flask, send_file

import os

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.inspection import inspect
from sqlalchemy.dialects import postgresql
#from sqlalchemy import db.db.db.mapped_column, Table, Column, Bigdb.Integer, db.Integer, db.db.Text, db.Date, db.Boolean, db.db.db.String, ForeignKey
from sqlalchemy import desc, text

import csv
import io
#from io import StringIO
from flask import make_response

import csv
from io import StringIO
#import StringIO       # allows you to store response object in memory instead of on disk
from flask import Flask, make_response # Necessary imports, should be obvious

from sqlalchemy import text

from openpyxl import Workbook
from flask import Response
from sqlalchemy import inspect

from sqlalchemy import column
import datetime
#from flask_http_response import success, result, error

#from app.models import DataModelTbl #inherits from DB.Model
#from db import DataModelTbl #inherits from DB.Model

from flask import Response
from openpyxl import Workbook
#from openpyxl.writer.excel import save_virtual_workbook
import flask_excel as excel


import pandas as pd
import io
from flask import make_response

from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from odf.opendocument import OpenDocumentSpreadsheet
from odf.table import Table, TableRow, TableCell
from odf.text import P
"""
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'  # Using SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define a sample model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
"""
# Initialize the database with some data
"""
@app.before_first_request
def create_tables():
    db.create_all()
    if not User.query.first():
        db.session.add_all([
            User(name="Alice", email="alice@example.com"),
            User(name="Bob", email="bob@example.com"),
            User(name="Charlie", email="charlie@example.com")
        ])
        db.session.commit()
"""
# Route to export data to ODS format

from ..auth.models import TUser

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, MetaData
from io import BytesIO
from odf.table import Table

@test_excel.route('/export-to-ods', methods=['GET'])

def export_to_ods():
    users = TUser.query.all()
    
    # Create a new ODS document
    doc = OpenDocumentSpreadsheet()
    table = Table()  # Correct usage
    table.setAttribute("name", "t_user")  # Naming the table
    doc.spreadsheet.addElement(table)
    
    # Add headers
    headers = ["ID", "Name", "Email"]
    header_row = TableRow()
    for header in headers:
        cell = TableCell()
        cell.addElement(P(text=header))
        header_row.addElement(cell)
    table.addElement(header_row)
    
    # Add data rows
    for user in users:
        data_row = TableRow()
        values = [user.id, user.username, user.email]
        for value in values:
            cell = TableCell()
            cell.addElement(P(text=str(value)))
            data_row.addElement(cell)
        table.addElement(data_row)
    
    # Save document to an in-memory BytesIO stream
    ods_stream = BytesIO()
    doc.save(ods_stream)
    ods_stream.seek(0)  # Rewind the stream to the beginning
    
    # Create a Flask response
    response = make_response(ods_stream.read())
    response.headers['Content-Disposition'] = 'attachment; filename=users.ods'
    response.mimetype = 'application/vnd.oasis.opendocument.spreadsheet'
    return response





@test_excel.route('/testods')
def testods():
    with db.engine.begin() as conn:
        ResultSet = conn.execute(text("SELECT * from t_user"))
#" {'deb': '20240307', 'fin': '20240320'}")

        rows = ResultSet.fetchall()
        keys = ResultSet.keys()
        #rows = ResultSet._metadata.keys
        data = rows

   
        # Convert result set to pandas data frame and add columns
        df = pd.DataFrame((tuple(t) for t in data),
            columns=keys)

        #df.to_excel('output.ods', engine='odf')
        
        # Creating output and writer (pandas excel writer)
        out = io.BytesIO()
        writer = pd.ExcelWriter(out, engine='xlsxwriter')

        #writer.save()
        writer.close()

   
        # Flask create response 
        r = make_response(out.getvalue())

    
        # Defining correct excel headers
        r.headers["Content-Disposition"] = "attachment; filename=export.xlsx"
        r.headers["Content-type"] = "application/x-xls"

    
        # Finally return response
        return r


@test_excel.route('/testexcel')
def testexcel():
    # create a random Pandas dataframe
    df_1 = pd.DataFrame(np.random.randint(0, 10, size=(10, 4)), columns=list('ABCD'))

    # create an output stream
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')

    # taken from the original question
    df_1.to_excel(writer, startrow=0, merge_cells=False, sheet_name="Sheet_1")
    workbook = writer.book
    worksheet = writer.sheets["Sheet_1"]
    format = workbook.add_format()
    format.set_bg_color('#eeeeee')
    worksheet.set_column(0, 9, 28)

    # the writer has done its job
    writer.close()

    # go back to the beginning of the stream
    output.seek(0)

    # finally return the file with the correct argument 'download_name'
    return send_file(output, download_name="testing.xlsx", as_attachment=True)
