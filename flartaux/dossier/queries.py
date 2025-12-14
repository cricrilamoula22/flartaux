"""
from .models import Item

def get_items_by_user_id(user_id):
    return Item.query.filter_by(user_id=user_id).all()

def get_item_by_id(item_id):
    return Item.query.get(item_id)
"""
from flask import session
from models import TDemande, TUsager
#TCadastre, TParceldem, TCom2023, TCadastre, 
#from models import TUser    
    
def fetch_dossiers_by_id(user_id):

    dossiers = TDemande.query.filter_by(user_id=user_id).order_by(desc(TDemande.no_interne)).all()

    dossiers_list = []
    for dossier in dossiers:
        dossiers_list.append({
            'no_interne': dossier.no_interne,
            'date_de_depot': dossier.date_de_depot,
            'no_pacage_demandeur': dossier.no_pacage_demandeur,            
            'u_nom_raison_sociale': dossier.u_nom_raison_sociale,            
        })

    return dossiers_list
    
def fetch_dossiers_by_no_interne(no_interne):
    
    dossiers = db.session.query(TDemande, TUsager
        ).filter(TDemande.no_interne == no_interne
        ).join(TUsager, TUsager.u_pacage == TDemande.no_pacage_demandeur
        ).with_entities(TDemande.no_interne, TDemande.date_de_depot,\
        TDemande.no_pacage_demandeur, TUsager.u_nom_raison_sociale 
        ).all()
    
    '''
    dossiers = db.session.query(TDemande
        ).filter(TDemande.no_interne == no_interne
        ).with_entities(TDemande.no_interne, TDemande.date_de_depot 
        ).all()
    '''
    dossiers_list = []
    for dossier in dossiers:
        dossiers_list.append({
            'no_interne': dossier.no_interne,
            'date_de_depot': dossier.date_de_depot,
            'no_pacage_demandeur': dossier.no_pacage_demandeur,            
            'u_nom_raison_sociale': dossier.u_nom_raison_sociale,
        })

    return dossiers_list
    

def get_dossier():
    #if 'user' in session:
    if current_user.is_authenticated:
        #user_id = current_user.id
        #username=current_user.username
        user_id = current_user.id
        no_interne = str(request.form.get('no_interne'))
        #cache.set("current_no_interne", no_interne)
        flash('test :' , str(no_interne))
        print('order_id:', str(no_interne))
        return db.session.query(TDemande).where(TDemande.no_interne == str(no_interne))
    return db.session.query(TDemande).where(TDemande.no_interne == str(no_interne)) 
    
