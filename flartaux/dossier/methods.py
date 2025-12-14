#from .models import Item
#from .models import TDemande
#from ..database import db
"""
def create_item(name, description, user_id):
    item = Item(name=name, description=description, user_id=user_id)
    db.session.add(item)
    db.session.commit()
    return item

def update_item(item, name, description):
    item.name = name
    item.description = description
    db.session.commit()
    return item

def delete_item(item):
    db.session.delete(item)
    db.session.commit()
"""    
def insertdoss():
    if request.method == 'POST':
        '''
        t_parceldem = get_all_parceldem()
        order_details = get_all_order_details()
        products = get_all_products()
        t_com2023 = get_all_t_com2023()
        parcelles = get_all_parcelles()
        all_data = db.session.query(TCadastre).filter(TCadastre.idsuf.like('220010000A%')).all() 
        form = Form()   
        fv = flask.__version__
        pv = platform.python_version()
        name = session['user']['name']
        userId = session['user']['id']
        '''
        #idsuf = request.form['idsuf']

        no_interne = request.form['no_interne']
        date_complet = datetime.today().strftime('%d-%m-%y')
        #user_id = session['user']['user_id']   
        user_id = request.form['user_id']
        my_data = TDemande(no_interne=no_interne,date_complet=date_complet,user_id=user_id)
        
    
        db.session.add(my_data)
        db.session.commit()
  
        flash("Nouveau dossier ajouté avec succès !")
        return redirect(url_for('dossier.dossier'))
     
