"""
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_caching import Cache
from db_file import db, login

import os
from flask import Flask, Blueprint, render_template

templates = os.path.join(os.path.dirname(__file__), 'templates')

parsel_bp = Blueprint('parsel', __name__, template_folder='templates', static_folder='static')


from parsel import routes
"""
"""
from flask import Blueprint

parsel_bp = Blueprint('parsel', __name__, template_folder='templates')

from . import routes
"""
from flask import Blueprint, render_template
import os
print(os.getcwd())


# Create the Blueprint instance
parsel = Blueprint('parsel', __name__, template_folder='templates/parsel')

#dossier = Blueprint('dossier', __name__)

# Import routes to connect with the Blueprint
from . import routes
