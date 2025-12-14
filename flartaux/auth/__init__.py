from flask import Blueprint, render_template
import os
print(os.getcwd())


# Create the Blueprint instance
auth = Blueprint('auth', __name__, template_folder='templates/auth')

# Import routes to connect with the Blueprint
from . import routes
