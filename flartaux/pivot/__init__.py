from flask import Blueprint, render_template
import os
print(os.getcwd())


# Create the Blueprint instance
pivot = Blueprint('pivot', __name__, template_folder='pivot/templates')

# Import routes to connect with the Blueprint
from . import routes
#init_zut(app)