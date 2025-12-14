#from .models import Item
from ..database import db
from .models import TCadastre, TParceldem, TCom2023
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
def total_balance():

    no_interne = str(session.get('no_interne'))

    return db.session.query(sum(int(str(TParceldem.par_surface)))).filter(TParceldem.par_nointerne.like(no_interne)).all()
    
def header():
    #pv = print(sys.version)
    #pv = print(platform.python_version())
    fv = flask.__version__
    pv = platform.python_version()
    return render_template('header.html', fv=fv, pv=pv)  # return index.html with username of logged user
    