from flask import Flask, Blueprint, render_template, Request
from jinja2 import FileSystemLoader
from flask import Flask, request, redirect, url_for, session, flash, jsonify, json
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from sqlalchemy.sql import text
from sqlalchemy import desc, asc, and_, select, text, or_, func

from wtforms import SelectField
from flask_wtf import FlaskForm

from flask import Blueprint, render_template

groupsel = Blueprint('groupsel', __name__, url_prefix='/groupsel', static_folder='static', template_folder='groupsel/templates')
from . import groupsel

from extensions import db
from extensions import cache


from flask import Flask, redirect, url_for, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from models import TProprietaires, TPropDem, Groups, LeftItems, RightItems, ItemsGroups
from models import TParceldem, TCadastre, TCadDem
from models import Users
import random
import string
import logging
from sqlalchemy import and_, or_, not_
import re
import pandas as pd
from sqlalchemy import select, literal

from sqlalchemy import select, func
from sqlalchemy.sql import over
from sqlalchemy.orm import aliased

@groupsel.route('/render_selected_items/<int:group_id>')
def render_selected_items(group_id):
    group = Group.query.get(group_id)
    selected_left_items = Item.query.filter_by(idprocpte=group.name, column_type='left').all()
    selected_right_items = Item.query.filter_by(idprocpte=group.name, column_type='right').all()
    return render_template('partials/selected_items.html', group=group, selected_left_items=selected_left_items, selected_right_items=selected_right_items)

   
@groupsel.route('/add_item', methods=['POST'])
def add_item():
    item_name = request.form['item_name']
    column_type = request.form['column_type']
    
    logging.debug(f"Adding item: {item_name}, column_type: {column_type}")

    # Create new item depending on the column type
    if column_type == 'left':
        new_item = LeftItem(name=item_name)
        db.session.add(new_item)
        db.session.commit()
        return jsonify({'id': new_item.id, 'name': new_item.name})
    
    elif column_type == 'right':
        #new_item = RightItem(name=item_name)
        no_interne = str(session.get('no_interne'))
        new_item = TProprietaires(ddenom=item_name, idprocpte=f"'{no_interne}_UNDEFINED")
        db.session.add(new_item)
        db.session.commit()
        return jsonify({'id': new_item.idt_proprietaires, 'name': new_item.ddenom})

    return jsonify({"error": "Invalid column type"}), 400


@groupsel.route('/add_group', methods=['POST'])
def add_group():
    random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    new_group = Group(name=random_name)
    db.session.add(new_group)
    db.session.commit()
    return jsonify({'group_name': random_name, 'group_id': new_group.id})



@groupsel.route('/add_item_to_group', methods=['POST'])
def add_item_to_group():
    item_name = request.form['item_name']
    group_id = request.form['group_id']
    column_type = request.form['column_type']
    group_name = Group.query.filter_by(id=group_id).first()
    
    logging.debug(f"Adding item to group: {item_name}, group_id: {group_id}, column_type: {column_type}")

    # Check if group exists
    group = db.session.query(Group).filter_by(id=group_id).first()
    if not group:
        logging.error("Group not found")
        return jsonify({"error": "Group not found"}), 404

    # Get the highest current selection order
    max_order = db.session.query(db.func.max(ItemGroup.selection_order)).filter_by(group_id=group_id).scalar() or -1
    logging.debug(f"Current max selection_order for group {group_id}: {max_order}")


    # Determine field based on column_type
    #if column_type == "left":
    if '/' not in item_name:
        cadastre = TCadastre.query.filter_by(idsuf=item_name).first()
        # Reset idprocpte
        cadastre.idprocpte = f"{group.name}"
        try:
            db.session.commit()
            return jsonify({"message": "Unselected successfully", "idsuf": cadastre.idsuf})
        except Exception as e:
            db.session.rollback()
            logging.error(f"DB Error: {e}")
            return jsonify({"error": "Database error", "details": str(e)}), 500        
        
    #elif column_type == "right":
    elif '/' in item_name:    
        cadastre = TProprietaires.query.filter_by(ddenom=item_name).first()
        # Reset idprocpte
        cadastre.idprocpte = f"{group.name}"
        try:
            db.session.commit()
            return jsonify({"message": "Unselected successfully", "idsuf": cadastre.ddenom})
        except Exception as e:
            db.session.rollback()
            logging.error(f"DB Error: {e}")
            return jsonify({"error": "Database error", "details": str(e)}), 500         
    else:
        return jsonify({"error": "Invalid column type"}), 400

    if not cadastre:
        return jsonify({"error": "Item not found"}), 404
    
    
    # Commit the transaction
    db.session.commit()
    logging.debug(f"Added item to group with selection_order {selection_order}")

    return jsonify({'id': item_group.id, 'name': item_group.item_name})

from functools import wraps
def my_wrapper_function(_f):
    @wraps(_f)
    def _decorated_function(*args, **kwargs):

       flash(request.form.get('item_name'))

       return _f(*args, **kwargs)

    return _decorated_function


@groupsel.route('/select_item', methods=['POST'])
#@my_wrapper_function
def select_item():
    item_name = request.form['item_name']
    group_id = request.form['group_id']
    column_type = request.form['column_type']
    group_name = Group.query.filter_by(id=group_id).first()
    no_interne = str(session.get('no_interne'))
    
    if group_name:
        name = group_name.name  # Assuming 'name' is the field you're interested in
        #print(name)  # This will print the name
    else:
        print("Group not found")

    if '/' not in item_name:
        cadastre = TCadastre.query.filter_by(idsuf=item_name).first()
        # Reset idprocpte
        cadastre.idprocpte = name
        try:
            db.session.commit()
            return jsonify({"message": "Unselected successfully", "idsuf": cadastre.idsuf})
        except Exception as e:
            db.session.rollback()
            logging.error(f"DB Error: {e}")
            return jsonify({"error": "Database error", "details": str(e)}), 500        
        
    #elif column_type == "right":
    elif '/' in item_name:    
        cadastre = TProprietaires.query.filter_by(ddenom=item_name).first()
        # Reset idprocpte
        cadastre.idprocpte = name
        try:
            db.session.commit()
            return jsonify({"message": "Unselected successfully", "idsuf": cadastre.ddenom})
        except Exception as e:
            db.session.rollback()
            logging.error(f"DB Error: {e}")
            return jsonify({"error": "Database error", "details": str(e)}), 500         
    else:
        return jsonify({"error": "Invalid column type"}), 400

    if not cadastre:
        return jsonify({"error": "Item not found"}), 404
    

    # Ensure the group exists
    group = db.session.query(Group).filter_by(id=group_id).first()

    if not group:
        return jsonify({"error": "Group not found"}), 404

    # Get the highest current selection order for this group
    max_order = db.session.query(db.func.max(ItemGroup.selection_order)).filter_by(group_id=group_id).scalar() or -1

    # Insert the new item with the next selection order
    selection_order = max_order + 1


    #return redirect(url_for('index'))
    return render_template('index.html', data=data, name=name, new_idprocpte=new_idprocpte, idsuf=idsuf)



@groupsel.route('/unselect_item', methods=['POST'])
def unselect_item():
    item_name = request.form.get('item_name')
    group_id = request.form.get('group_id')
    column_type = request.form.get('column_type')
    #results = MyModel.query.filter(MyModel.path.contains('/')).all()

    logging.debug(f"Unselecting item: {item_name} from group {group_id} ({column_type})")

    group_name = Group.query.filter_by(id=group_id).first()
    no_interne = str(session.get('no_interne'))
    
    if group_name:
        name = group_name.name  # Assuming 'name' is the field you're interested in
        #print(name)  # This will print the name
    else:
        print("Group not found")
    if not group_name:
        return jsonify({"error": "Group not found"}), 404

    # Determine field based on column_type
    #if column_type == "left":
    if '/' not in item_name:
        cadastre = TCadastre.query.filter_by(idsuf=item_name).first()
        # Reset idprocpte
        cadastre.idprocpte = f"'{no_interne}_UNDEFINED"
        try:
            db.session.commit()
            return jsonify({"message": "Unselected successfully", "idsuf": cadastre.idsuf})
        except Exception as e:
            db.session.rollback()
            logging.error(f"DB Error: {e}")
            return jsonify({"error": "Database error", "details": str(e)}), 500        
        
    #elif column_type == "right":
    elif '/' in item_name:
        cadastre = TProprietaires.query.join(Group, TProprietaires.idprocpte==name)\
        .filter(and_(TProprietaires.ddenom==item_name, TProprietaires.idprocpte==name)).all()

    if not cadastre:
        return jsonify({"error": "Item not found"}), 404

    updated_items = []
    for entry in cadastre:
        entry.idprocpte = f"'{no_interne}_UNDEFINED"
        updated_items.append(entry.ddenom)

    try:
        db.session.commit()
        return jsonify({"message": "Unselected successfully", "idsuf": updated_items})
    except Exception as e:
        db.session.rollback()
        logging.error(f"DB Error: {e}")
        return jsonify({"error": "Database error", "details": str(e)}), 500
    else:
        return jsonify({"error": "Invalid column type"}), 400



@groupsel.route('/left_items', methods=['GET'])
def get_left_items():
    no_interne = str(session.get('no_interne'))
    # Fetch available left items
    #available_left_items = TUser.query.all()
    #available_left_items = TParceldem.query.filter(TParceldem.par_nointerne == 'C22250048').order_by(TParceldem.par_idsuf.desc()).all()
    """
    available_left_items = db.session.query(TProprietaires)\
    .join(TProprietaires, TCadastre.idsuf == TParceldem.par_idsuf)\
    .join(TProprietaires, TProprietaires.idprocpte == TCadastre.idprocpte)\
    .filter(and_(TCadastre.idprocpte.is_('%_UNDEFINED'), TParceldem.par_nointerne == no_interne))\
    .order_by(TCadastre.idsuf).all()
    """
    available_left_items = db.session.query(TParceldem)\
    .join(TCadastre, TCadastre.idsuf == TParceldem.par_idsuf)\
    .join(Group, TCadastre.idprocpte == Group.name)\
    .join(TProprietaires, TProprietaires.idprocpte == Group.name)\
    .with_entities(TCadastre.idprocpte, TProprietaires.ddenom, TParceldem.par_idsuf)\
    .filter(and_(TParceldem.par_nointerne == no_interne, TCadastre.idsuf == TParceldem.par_idsuf), not_(TCadastre.idprocpte.contains('_UNDEFINED')))\
    .group_by(TCadastre.idprocpte, TProprietaires.ddenom, TParceldem.par_idsuf)\
    .order_by(TParceldem.par_idsuf).distinct(TParceldem.par_idsuf).all()
    available_left_items_names = [item.par_idsuf for item in available_left_items]
    
    # Get the currently selected left items
    #selected_left_items = db.session.query(TUser).all()
    #selected_left_items = db.session.query(TParceldem).filter(TParceldem.par_nointerne == 'C22250048').order_by(TParceldem.par_idsuf.desc()).all()
    selected_left_items = db.session.query(TProprietaires).join(TProprietaires, TCadastre.idsuf == TParceldem.par_idsuf)\
    .join(TProprietaires, or_(TProprietaires.idprocpte == TCadastre.idprocpte, TCadastre.idprocpte == no_interne))\
    .filter(TParceldem.par_nointerne == no_interne, TCadastre.idprocpte.is_('INCONNU'))\
    .order_by(TParceldem.par_idsuf).all()
    selected_left_item_names = [item.par_idsuf for item in selected_left_items]
    """
    # Filter out selected items from available items
    available_left_items = [item for item in available_left_items if item.username in selected_left_item_names]
    """

    return jsonify({'items': [{'id': item.idprocpte, 'name': item.par_idsuf} for item in available_left_items]})

@groupsel.route('/right_items', methods=['GET'])
def get_right_items():
    no_interne = str(session.get('no_interne'))
    available_right_items = TProprietaires.query\
    .join(TCadastre, TCadastre.idsuf == TParceldem.par_idsuf)\
    .join(Group, TProprietaires.idprocpte == Group.name)\
    .join(TProprietaires, or_(TProprietaires.idprocpte == TCadastre.idprocpte, TProprietaires.idprocpte == f"'{no_interne}_UNDEFINED"))\
    .filter(and_(TParceldem.par_nointerne == no_interne, TProprietaires.idprocpte == f"'{no_interne}_UNDEFINED"))\
    .order_by(asc(TProprietaires.ddenom))\
    .distinct(TProprietaires.ddenom).all()
    #available_right_items = RightItem.query.all()
    available_right_items_names = [item.ddenom for item in available_right_items]
    #available_right_items_names = [item.name for item in available_right_items]
    
    # Get the currently selected left items
    selected_right_items = TParceldem.query\
    .join(TCadastre, TCadastre.idsuf == TParceldem.par_idsuf)\
    .join(TProprietaires, TProprietaires.idprocpte == TCadastre.idprocpte)\
    .with_entities(TProprietaires.idprocpte, TProprietaires.ddenom, TParceldem.par_idsuf)\
    .filter(TParceldem.par_nointerne == no_interne).order_by(TParceldem.par_idsuf).all()
    #selected_right_items = db.session.query(ItemGroup).filter(ItemGroup.column_type == 'right').all()
    selected_right_item_names = [item.ddenom for item in selected_right_items]
    #selected_right_item_names = [item.item_name for item in selected_right_items]
    
    # Filter out selected items from available items
    #available_right_items = [t_proprietaires for t_proprietaires in available_right_items if t_proprietaires.ddenom not in selected_right_item_names]

    #return jsonify({'t_proprietaires': [{'t_proprietaires': t_proprietaires.ddenom, 't_proprietaires': t_proprietaires.ddenom} for t_proprietaires in available_right_items]})
    return jsonify({'items': [{'id': item.idprocpte, 'name': item.ddenom} for item in available_right_items]})

@groupsel.route('/groupsel')
def groupsel():

    #group_name = Group.query.filter_by(id=group_id).first()
    no_interne = str(session.get('no_interne'))
    subquery = db.session.query(TParceldem).join(TCadDem, TCadDem.idsuf == TParceldem.par_idsuf)\
    .join(TPropDem, or_(TPropDem.idprocpte == TCadDem.idprocpte, TPropDem.idprocpte.contains('_UNDEFINED'))).with_entities(TCadDem.idprocpte)\
    .filter(TParceldem.par_nointerne == no_interne)\
    .order_by(TParceldem.par_idsuf).subquery()
    #groups = db.session.query(Group).filter(Group.name.in_(subquery)).order_by(Group.name.desc()).all()
    groups = db.session.query(Groups).filter(Groups.name.in_(subquery.select())).order_by(Groups.name.desc()).all()


    #selected_left_items = db.session.query(TUser).order_by(TUser.username.desc()).all()
    #selected_left_items = db.session.query(TParceldem).filter(TParceldem.par_nointerne == 'C22250048').order_by(TParceldem.par_idsuf.desc()).all()
    """
    selected_left_items = db.session.query(TParceldem)\
    .join(Group, TCadastre.idprocpte == Group.name)\
    .join(TCadastre, or_(TCadastre.idprocpte == func.concat('\'', no_interne, '_UNDEFINED'), TCadastre.idprocpte == Group.name))\
    .with_entities(TParceldem.par_idsuf)\
    .filter(and_(TParceldem.par_nointerne == no_interne, TCadastre.idsuf == TParceldem.par_idsuf), not_(TCadastre.idprocpte.contains('_UNDEFINED')))\
    .group_by(TParceldem.par_idsuf)\
    .order_by(asc(TParceldem.par_idsuf)).distinct(TParceldem.par_idsuf).all()
    
    selected_left_items = db.session.query(TParceldem).join(TCadastre, TCadastre.idsuf == TParceldem.par_idsuf)\
    .join(TProprietaires, or_(TProprietaires.idprocpte == TCadastre.idprocpte)).with_entities(TProprietaires.idprocpte, TProprietaires.ddenom, TParceldem.par_idsuf)\
    .filter(and_(TParceldem.par_nointerne == no_interne, TCadastre.idsuf == TParceldem.par_idsuf), not_(TCadastre.idprocpte.contains('_UNDEFINED')))\
    .group_by(TProprietaires.idprocpte, TProprietaires.ddenom, TParceldem.par_idsuf)\
    .order_by(TParceldem.par_idsuf).distinct(TParceldem.par_idsuf).all()
    """
    selected_left_items = db.session.query(TParceldem)\
    .join(TCadDem, TCadDem.idsuf == TParceldem.par_idsuf)\
    .join(Groups, TCadDem.idprocpte == Groups.name)\
    .with_entities(TCadDem.idprocpte, TParceldem.par_idsuf)\
    .filter(and_(TParceldem.par_nointerne == no_interne, TCadDem.idsuf == TParceldem.par_idsuf), not_(TCadDem.idprocpte.contains('_UNDEFINED')))\
    .group_by(TCadDem.idprocpte, TParceldem.par_idsuf)\
    .order_by(TParceldem.par_idsuf).distinct(TParceldem.par_idsuf).all()
    #.join(TProprietaires, or_(TProprietaires.idprocpte == TCadastre.idprocpte))
    for item in selected_left_items:
        print(f"ID: Email: {item.par_idsuf}")
    
    results = (
        db.session.query(
            TPropDem.idprocpte,
            TPropDem.ddenom
        )
        .join(TCadDem, TPropDem.idprocpte == TCadDem.idprocpte)
        .join(TParceldem, TCadDem.idsuf == TParceldem.par_idsuf)
        .filter(TParceldem.par_nointerne == no_interne)
        .all()
    )

    seen = set()
    unique_right_items = []

    for idprocpte, ddenom in results:
        key = (idprocpte, ddenom)
        if key not in seen:
            seen.add(key)
            unique_right_items.append({
                "idprocpte": idprocpte,
                "ddenomsansdoublon": ddenom
            })


    #selected_right_items = stmt.all()
    selected_right_items = unique_right_items
    #selected_right_items = db.session.query(ItemGroup).filter(ItemGroup.column_type == 'right').order_by(ItemGroup.selection_order.desc()).all()
    """
    selected_right_items = db.session.query(TParceldem).join(TCadastre, TCadastre.idsuf == TParceldem.par_idsuf)\
    .join(TProprietaires, TProprietaires.idprocpte == TCadastre.idprocpte)\
    .with_entities(TProprietaires.idprocpte, TProprietaires.ddenom, TParceldem.par_idsuf)\
    .group_by(TCadastre.idprocpte, TParceldem.par_idsuf, TProprietaires.ddenom, TProprietaires.idprocpte)\
    .filter(TParceldem.par_nointerne == no_interne, TCadastre.idsuf == TParceldem.par_idsuf)\
    .order_by(asc(TCadastre.idprocpte), asc(TProprietaires.ddenom)).all()
    """
    #.distinct(TProprietaires.ddenom)
    #.group_by(TCadastre.idprocpte, TParceldem.par_idsuf, TProprietaires.idprocpte, TProprietaires.ddenom)\    
    """
    for item in selected_right_items:

        print(f"ID: {item.idprocpte}, Name: {item.ddenomsansdoublon}")
        #print(f"ID: {TProprietaires.idprocpte}, Name: {item.ddenom}, Email: {TParceldem.par_idsuf}")
    """    
    #selected_left_item_names = [item.username for item in selected_left_items]
    selected_left_item_names = [item.par_idsuf for item in selected_left_items]
    #selected_right_item_names = [item.ddenom for item in selected_right_items]
    selected_right_item_names = [item["ddenomsansdoublon"] for item in selected_right_items]


    #left_items = TUser.query.filter(~TUser.username.in_(selected_left_item_names)).all()
    no_interne = session.get('no_interne')
    mince = f"'{no_interne}_UNDEFINED"
    print("mince :", mince)
    
    no_interne_value = session.get('no_interne')  # This is still a string, right?
    stmt = select(func.concat("'", no_interne_value, "_UNDEFINED"))
    result = db.session.execute(stmt).scalar()
    print("mince:", result)

    left_items = TParceldem.query\
    .join(TCadDem, TCadDem.idsuf == TParceldem.par_idsuf)\
    .filter(TCadDem.idprocpte == f"'{no_interne}_UNDEFINED")\
    .order_by(TParceldem.par_idsuf.desc()).all()
    """
    left_items = db.session.query(TParceldem)\
    .join(TCadastre, TCadastre.idsuf == TParceldem.par_idsuf)\
    .join(Group, TCadastre.idprocpte == Group.name)\
    .with_entities(TCadastre.idprocpte, TParceldem.par_idsuf)\
    .filter(and_(TParceldem.par_nointerne == no_interne, TCadastre.idsuf == TParceldem.par_idsuf), not_(TCadastre.idprocpte.contains('_UNDEFINED')))\
    .group_by(TCadastre.idprocpte, TParceldem.par_idsuf)\
    .order_by(TParceldem.par_idsuf).distinct(TParceldem.par_idsuf).all()
    """
    #left_items = TParceldem.query.filter(TParceldem.par_idsuf.in_(selected_right_item_names)).all()
    #right_items = RightItem.query.filter(~RightItem.name.in_(selected_right_item_names)).all()
    right_items = TParceldem.query\
    .join(TCadDem, TCadDem.idsuf == TParceldem.par_idsuf)\
    .join(TPropDem, or_(TPropDem.idprocpte == TCadDem.idprocpte, TPropDem.idprocpte == func.concat('\'', no_interne, '_UNDEFINED')))\
    .join(Groups, or_(TPropDem.idprocpte == Groups.name, TPropDem.idprocpte == func.concat('\'', no_interne, '_UNDEFINED')))\
    .with_entities(TPropDem.ddenom)\
    .filter(and_(TParceldem.par_nointerne == no_interne, TPropDem.idprocpte.in_([TCadDem.idprocpte, func.concat('\'', no_interne, '_UNDEFINED')])))\
    .order_by(asc(TPropDem.ddenom)).distinct(TPropDem.ddenom).all()
   
    return render_template('groupsel/groupsel.html', left_items=left_items, right_items=right_items, groups=groups, selected_left_items=selected_left_items, selected_right_items=unique_right_items)
