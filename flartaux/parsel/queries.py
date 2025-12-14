from .models import TCadastre, TParceldem, TCom2023
from flask import session
from ..database import db
from ..extensions import cache
"""
from .models import Item

def get_items_by_user_id(user_id):
    return Item.query.filter_by(user_id=user_id).all()

def get_item_by_id(item_id):
    return Item.query.get(item_id)
"""
def get_parcelle_by_idsuf(idsuf):
    return db.session.query(TCadastre).get(idsuf)

def get_all_t_demande():
    return db.session.query(TDemande).all()

def get_all_parcelles():
    return db.session.query(TCadastre).filter(TCadastre.idsuf.like("99999%")).order_by(TCadastre.idsuf.desc()).all()

def get_all_parceldem():
    #no_interne = cache.get("no_interne")
    no_interne = str(session.get('no_interne'))
    #par_surface = str(TParceldem.par_surface)
    #par_surface = str(cast(trim(trailing '0' from replace(par_surface, ',', '')::text) as int))
    #import numpy as np
    #par_surface = np.round(TParceldem.par_surface,3).astype(str)
    #par_surface = np.rint(TParceldem.par_surface)
    #par_surface = int([TParceldem.par_surface).strip())
    
    from sqlalchemy import case, cast, Numeric, func
    from decimal import Decimal
    
    # Assuming TParceldem.par_surface is a column of type string or other non-numeric types
    result = db.session.query(
        func.round(
            case(
                (cast(func.replace(TParceldem.par_surface, ',','.'), Numeric).isnot(None), cast(func.replace(TParceldem.par_surface, ',','.'), Numeric)),
                else_=0  # Default to 0 if not numeric
            ),
            4  # Round to 2 decimal places
        )
    ).first()

    if result:
        #par_surface = str(Decimal(result[0]) * 1000)
        #par_surface = str(Decimal(result[0]))
        par_surface = str(Decimal(result[0]) / 10000)
        #print(result[0])  # The rounded result

    
    #par_surface = str(Decimal(db.session.query(TParceldem.par_surface).first()) * 10000)
    #par_surface = str(Decimal(TParceldem.par_surface) * 10000)
    return db.session.query(TParceldem).filter(TParceldem.par_nointerne.like(no_interne)).order_by(TParceldem.par_idsuf.desc()).all()

def get_all_t_com2023():
    return db.session.query(TCom2023).filter(TCom2023.dep == '22').all()

    
def fetch_sections_by_commune(idcom):
    sections = db.session.query(TCadastre.ccosec.distinct()).where(TCadastre.idcom=='22278').all()

    sections_list = []
    for section in sections:
        sections_list.append({
            #'idcom': request.form['res'],
            'ccosec': TCadastre.ccosec
            #'idsuf': TCadastre.idsuf
        })

    return sections_list

def fetch_dossiers_by_id(user_id):
    """
    Fetch orders from the database by user ID.

    Args:
        user_id (int): The ID of the user to fetch orders for.

    Returns:
        list: A list of orders for the given user ID.
    """
    dossiers = TDemande.query.filter_by(user_id=user_id).order_by(desc(TDemande.no_interne)).all()

    dossiers_list = []
    for dossier in dossiers:
        dossiers_list.append({
            'no_interne': dossier.no_interne,
            'date_de_depot': dossier.date_de_depot
        })

    return dossiers_list
    
def fetch_dossiers_by_no_interne(no_interne):
    """
    Fetch orders from the database by user ID.

    Args:
        user_id (int): The ID of the user to fetch orders for.

    Returns:
        list: A list of orders for the given user ID.
    """
    dossiers = db.session.query(TDemande, TUsager
        ).filter(TDemande.no_interne == no_interne
        ).join(TUsager, TUsager.u_pacage == TDemande.no_pacage_demandeur
        ).with_entities(TDemande.no_interne, TDemande.date_de_depot,\
        TDemande.no_pacage_demandeur, TUsager.u_nom_raison_sociale 
        ).all()
    dossiers_list = []
    for dossier in dossiers:
        dossiers_list.append({
            'no_interne': dossier.no_interne,
            'date_de_depot': dossier.date_de_depot,
            'no_pacage_demandeur': dossier.no_pacage_demandeur,
            'u_nom_raison_sociale': dossier.u_nom_raison_sociale
        })

    return dossiers_list
    

# this method authenticate user with username and password
def authenticate_user(email, password):
    """
    Authenticates user with email & password.

    This method chec if the provided email and password match any users
    credentials stored in DB

    Args:
        email (str):  email to authenticate.
        password (str): password to authenticate.

    Returns:
       user:  if the email and password match, ifnot otherwise.
    """

    # Retrieve the user details based on the provided email
    user = UserDetails.query.filter_by(email=email).first()

    # Check if a user with the provided email exists and if the password matches
    if user and user.check_password(password):
        return {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role
        }
    else:
        return None


def insert_default_products():
    default_products = [
        {"id": 1, "name": "iphone 15 pro", "price": 1199.0, "image_name": "iphone-15-pro.png"},
        {"id": 2, "name": "Oneplus 9", "price": 799.0, "image_name": "oneplus-9.png"},
        {"id": 3, "name": "Samsung S24 ultra", "price": 1299.0, "image_name": "s24-ultra.png"},
        {"id": 4, "name": "Xiaomi mi 11", "price": 599.0, "image_name": "xiaomi-mi-11.png"},
        {"id": 5, "name": "iPhone 13 pro", "price": 1000.0, "image_name": "iphone 13 pro.jpeg"}
    ]

    for product in default_products:
        existing_product = Product.query.filter_by(id=product["id"]).first()
        if not existing_product:
            new_product = Product(
                id=product["id"],
                name=product["name"],
                price=product["price"],
                image_name=product["image_name"]
            )
            db.session.add(new_product)
    db.session.commit()
