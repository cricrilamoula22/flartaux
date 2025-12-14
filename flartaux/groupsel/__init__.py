from flask import Blueprint, render_template
import os
print(os.getcwd())


# Create the Blueprint instance
groupsel = Blueprint('groupsel', __name__, template_folder='groupsel/templates')

# Import routes to connect with the Blueprint
from . import routes
#init_zut(app)