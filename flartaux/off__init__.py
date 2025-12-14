from flask import Flask, Blueprint, render_template, request, current_app
from flask_caching import Cache
from .config import Config
from .extensions import db, migrate, login_manager, cache

#from .dossier.routes import dossier_blueprint
#from . import dossier  # Import the dossier blueprint
#from .dossier.routes import dossier
from .auth.models import TUser
#from . import parsel  # Import the dossier blueprint
#from .parsel.routes import parsel
#from .parsel.routes import parsel_blueprint

def create_app():
    app = Flask(__name__, template_folder='templates')  
    # Clear template cache
    app.jinja_env.cache.clear()
    print("Cache cleared!")
    
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        db.create_all()
    login_manager.init_app(app)
    # Configuring cache, you can replace with a different backend as necessary
    #app.config['CACHE_TYPE'] = 'simple'
    cache.init_app(app)  # This initializes the cache object for the app
    """
    @app.route('/')
    @cache.cached(timeout=60)  # Cache the view for 60 seconds
    def index():
        # Simulate dynamic content (e.g., a timestamp or a dynamic value)
        dynamic_data = "This page is cached for 60 seconds. Time: " + str(time.time())
    return render_template('test.html', dynamic_data=dynamic_data)
    """
    
    @login_manager.user_loader
    def load_user(user_id):
        return TUser.query.get(int(user_id))    
    
    # Register Blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .zut import zut as zut_blueprint
    app.register_blueprint(zut_blueprint)
    
    from .groupsel import groupsel as groupsel_blueprint
    app.register_blueprint(groupsel_blueprint, url_prefix='/', static_folder='static', template_folder='groupsel/templates')

    from .pivot import pivot as pivot_blueprint
    app.register_blueprint(pivot_blueprint, url_prefix='/', static_folder='static', template_folder='pivot/templates')

    from .control import control as control_blueprint
    app.register_blueprint(control_blueprint, url_prefix='/', static_folder='static', template_folder='control/templates')

    from .tree import tree as tree_blueprint
    app.register_blueprint(tree_blueprint, url_prefix='/', static_folder='static', template_folder='tree/templates')
      
    from .test_excel import test_excel as test_excel_blueprint
    app.register_blueprint(test_excel_blueprint)
    
    from .book_list import book_list as book_list_blueprint
    app.register_blueprint(book_list_blueprint)
    
    from .export_pandas_excel import export_pandas_excel as export_pandas_excel_blueprint
    app.register_blueprint(export_pandas_excel_blueprint)

    from .excel import excel as excel_blueprint
    app.register_blueprint(excel_blueprint)
        
    from .templdocx import templdocx as templdocx_blueprint
    app.register_blueprint(templdocx_blueprint, url_prefix='/', static_folder='static', template_folder='/templdocx/templates/templdocx')

    from .dossier import dossier as dossier_blueprint
    #from .dossier import dossier as dossier
    app.register_blueprint(dossier_blueprint)
    #app.register_blueprint(dossier_blueprint, url_prefix='/dossier')
    #app.register_blueprint(dossier, url_prefix='/dossier')
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    """
    from .parsel import parsel as parsel
    app.register_blueprint(parsel, url_prefix='/parsel', template_folder='templates/parsel')
    """
    #from .parsel import parsel as parsel_blueprint
    #app.register_blueprint(parsel_blueprint)
    
    return app
    

    
# app/auth/__init__.py
"""
# Import inside a function to avoid circular import at the module level
def init_auth(app):
    from . import routes  # Now import routes only when needed
    app.register_blueprint(routes.auth)
    
def init_dossier(app):
    from . import routes  # Now import routes only when needed
    app.register_blueprint(routes.dossier)
    
def init_zut(app):
    from . import routes  # Now import routes only when needed
    app.register_blueprint(routes.zut)
"""