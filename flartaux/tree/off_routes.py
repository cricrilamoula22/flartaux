'''
from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from extensions import db
from models import TreeCategories, UserSelections

tree = Blueprint('tree', __name__, url_prefix='/tree',
                 static_folder='static', template_folder='tree/templates')

@tree.route('/')
@login_required
def tree_page():
    return render_template('tree/treeview.html')
'''
from flask import Flask, Blueprint, render_template, Request
from jinja2 import FileSystemLoader
from flask import Flask, request, redirect, url_for, session, flash, jsonify, json
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from sqlalchemy.sql import text
from sqlalchemy import desc, asc, and_, select, text, or_, func

from wtforms import SelectField
from flask_wtf import FlaskForm

from flask import Blueprint, render_template
#dossier = Blueprint('dossier_blueprint', __name__)
tree = Blueprint('tree', __name__, url_prefix='/tree', static_folder='static', template_folder='tree/templates')
from . import tree
# Personnaliser le moteur de rendu de templates
#groupsel.jinja_loader = FileSystemLoader('/groupsel/templates/groupsel')

# Create the Blueprint instance
#dossier_blueprint = Blueprint('dossier_blueprint', __name__)

#init_zut(app)
"""
import os
print(os.getcwd())
print(app.jinja_loader.searchpath)
"""
from extensions import db
from extensions import cache
#from .queries import fetch_dossiers_by_no_interne, fetch_dossiers_by_id, get_parcelle_by_idsuf, get_all_t_demande, get_all_parcelles, get_all_parceldem, get_all_t_com2023, fetch_sections_by_commune
#from .models import TParceldem, TCom2023, TCadastre
#from .forms import Form

from flask import Flask, redirect, url_for, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
#from .models import db,
"""
from .models import TProprietaires, Group, LeftItem, RightItem, ItemGroup
from ..zut.models import TParceldem, TCadastre
from ..auth.models import TUser
"""
from models import TreeCategories, UserSelections
import random
import string
import logging
from sqlalchemy import and_, or_, not_
import re
import pandas as pd
from sqlalchemy import select, literal

from io import BytesIO

from flask import Flask, send_file
'''
@tree.route('/tree')
@login_required
def tree_page():
    #session['user_id'] = 1

    user_id = current_user.id
    print("user_id : ", user_id)

    return render_template('tree/treeview.html')
'''
@tree.route('/tree')
@login_required
def tree_page():
    return render_template('tree/treeview.html')

@tree.route('/api/tree')
def get_tree():
    # Racines = catégories sans parent
    roots = TreeCategories.query.filter_by(parent_id=None).all()
    return jsonify([r.to_dict() for r in roots])

@tree.route('/api/save-selections', methods=['POST'])
@login_required
def save_selections():
    data = request.get_json()
    user_id = current_user.id
    selected_ids = data.get('selected', [])

    # Supprimer anciennes sélections
    UserSelections.query.filter_by(user_id=user_id).delete()

    # Ajouter nouvelles sélections
    for cat_id in selected_ids:
        db.session.add(UserSelections(user_id=user_id, category_id=cat_id))

    db.session.commit()
    return jsonify({'status': 'success', 'saved': selected_ids})
