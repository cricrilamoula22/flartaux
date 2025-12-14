from flask import Flask, Blueprint, render_template, Request
from jinja2 import FileSystemLoader
from flask import Flask, request, redirect, url_for, session, flash, jsonify, json
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from sqlalchemy.sql import text
from sqlalchemy import desc, asc, and_, select, text, or_, func

from wtforms import SelectField
from flask_wtf import FlaskForm

from flask import Blueprint, render_template

tree = Blueprint('tree', __name__, url_prefix='/tree', static_folder='static', template_folder='tree/templates')
from . import tree

from extensions import db
from extensions import cache

from flask import Flask, redirect, url_for, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

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


@tree.route('/tree')
@login_required
def tree_page():
    #session['user_id'] = 1

    user_id = current_user.id
    print("user_id : ", user_id)

    return render_template('tree/treeview.html')

def to_dict(self):
    return {
        "id": self.id,
        "text": self.name,  # ← essentiel !
        "children": [child.to_dict() for child in self.children]
    }

'''
@tree.route('/api/tree')
def get_tree():
    roots = TreeCategories.query.filter_by(parent_id=None).all()
    return jsonify([r.to_dict() for r in roots])
'''
@tree.route('/api/tree')
def get_tree():

    def flatten(node):
        flat = [{
            "id": node.id,
            "text": node.name,
            "parent": "#" if node.parent_id is None else node.parent_id,
            "state": {"opened": True}  # optionnel
        }]
        for child in node.children:
            flat += flatten(child)
        return flat

    roots = TreeCategories.query.filter_by(parent_id=None).all()

    flat_tree = []
    for r in roots:
        flat_tree += flatten(r)

    return jsonify(flat_tree)
 
 
@tree.route('/api/save-selections', methods=['POST'])
def save_selections():
    data = request.get_json()
    #user_id = session.get(current_user.id)  # ✅ use session here
    user_id = current_user.id
    selected_ids = data.get('selected', [])

    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401

    # Delete old selections
    UserSelections.query.filter_by(user_id=user_id).delete()

    # Add new selections
    for cat_id in selected_ids:
        db.session.add(UserSelections(user_id=user_id, category_id=cat_id))

    db.session.commit()
    return jsonify({'status': 'success', 'saved': selected_ids})
