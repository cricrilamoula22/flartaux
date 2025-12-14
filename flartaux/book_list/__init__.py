"""
from flask import Blueprint

book_list_bp = Blueprint('book_list', __name__)#, template_folder='book_list/templates')

from . import routes
"""
from flask import Blueprint, render_template
import os
print(os.getcwd())


# Create the Blueprint instance
book_list = Blueprint('book_list', __name__, template_folder='templates/book_list')

# Import routes to connect with the Blueprint
from . import routes
