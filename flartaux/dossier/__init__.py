
"""
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_caching import Cache
from db_file import db, login
"""

# Initialize the Blueprint for authentication
"""
dossier_bp = Blueprint('dossier', __name__)

, url_prefix='/parsel',
                 template_folder='templates',
                 static_folder='static')

from dossier import routes
"""
"""
from flask import Blueprint

dossier_bp = Blueprint('dossier', __name__, template_folder='templates')

from . import routes
"""
from flask import Blueprint, render_template
import os
print(os.getcwd())


# Create the Blueprint instance
dossier = Blueprint('dossier', __name__, template_folder='templates/dossier')

#dossier = Blueprint('dossier', __name__)

# Import routes to connect with the Blueprint
from . import routes
