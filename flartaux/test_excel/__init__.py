"""
from flask import Blueprint

bp = Blueprint('parsel', __name__)

from app.parsel import routes

from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_caching import Cache
from db_file import db, login, cache
"""
# Initialize extensions
"""
db = SQLAlchemy()
login_manager = LoginManager()
cache = Cache()

# Initialize the Blueprint for authentication
export_pandas_excel_bp = Blueprint('export_pandas_excel', __name__)

, url_prefix='/parsel',
                 template_folder='templates',
                 static_folder='static')
"""
#from export_pandas_excel import routes

from flask import Blueprint, render_template
import os
print(os.getcwd())


# Create the Blueprint instance
test_excel = Blueprint('test_excel', __name__, template_folder='templates/test_excel')

# Import routes to connect with the Blueprint
from . import routes
