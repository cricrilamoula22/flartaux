from flask import Blueprint, render_template
import os
print(os.getcwd())


# Create the Blueprint instance
zut = Blueprint('zut', __name__, template_folder='templates/zut')

# Import routes to connect with the Blueprint
from . import routes
#init_zut(app)