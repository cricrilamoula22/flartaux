"""
from flask import Blueprint

templdocx_bp = Blueprint('templdocx', __name__, template_folder='templates')

from . import routes
"""
from flask import Blueprint, render_template
import os
print(os.getcwd())


# Create the Blueprint instance
templdocx = Blueprint('templdocx', __name__, template_folder='templates/templdocx')

# Import routes to connect with the Blueprint
from . import routes
#init_zut(app)