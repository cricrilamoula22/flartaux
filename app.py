from dotenv import load_dotenv
load_dotenv()

from flask import Flask, redirect
#from avis import avis_bp
from waitress import serve
from dotenv import load_dotenv
from os.path import join,dirname
from os import environ

from flask import Flask, Blueprint, render_template, request, current_app
from flask_caching import Cache
from config import Config
from extensions import db, migrate, login_manager, cache

from flask import Flask
from config import Config
#from models import db
from extensions import db
from extensions import cache
from flask_migrate import Migrate

#from flartaux.avis import avis

#from routes.avis import avis_bp
#from routes.main import main_bp
from routes.auth import auth_bp, login_manager
from routes.dashboard import dashboard_bp
from routes.transactions import transactions_bp
from routes.reports import reports_bp
from routes.categories import categories_bp
from routes.agent import agent_bp
from routes.main import main_bp
from routes.selection import selection_bp
#from routes.main import main as main_bp

#from flartaux.main import main as main_blueprint

#from flartaux.dossier import dossier as dossier_blueprint
from flartaux.dossier import dossier
from flartaux.control import control
from flartaux.zut import zut
from flartaux.groupsel import groupsel
from flartaux.book_list import book_list
from flartaux.tree import tree

from sqlalchemy import text

def realign_all_sequences(schema="w_sadr_artaux"):
    # Récupérer toutes les séquences du schéma
    sequences = db.session.execute(text(f"""
        SELECT seq.relname AS sequence_name,
               tbl.relname AS table_name,
               col.attname AS column_name
        FROM pg_class seq
        JOIN pg_namespace nsp ON seq.relnamespace = nsp.oid
        JOIN pg_depend dep ON dep.objid = seq.oid
        JOIN pg_class tbl ON dep.refobjid = tbl.oid
        JOIN pg_attribute col ON dep.refobjid = col.attrelid AND dep.refobjsubid = col.attnum
        WHERE seq.relkind = 'S'
          AND nsp.nspname = :schema
    """), {"schema": schema}).fetchall()

    for seq_name, table_name, column_name in sequences:
        full_seq = f"{schema}.{seq_name}"
        full_table = f"{schema}.{table_name}"
        sql = text(f"""
            SELECT setval('{full_seq}',
                          (SELECT COALESCE(MAX({column_name}), 1) FROM {full_table}) + 1,
                          false)
        """)
        db.session.execute(sql)

    db.session.commit()
    print(f"✅ Séquences du schéma {schema} réalignées")

     
def create_app():
    app = Flask(__name__, template_folder='templates')
    """
    @avis.route('/avis')
    def index():
        return render_template("generate.html")
    """
    # Clear template cache
    app.jinja_env.cache.clear()
    print("Cache cleared!")
    
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        db.create_all()
        # 🔧 réaligner toutes les séquences du schéma
        realign_all_sequences("w_sadr_artaux")
    login_manager.init_app(app)
    # Configuring cache, you can replace with a different backend as necessary
    app.config['CACHE_TYPE'] = 'simple'
    cache.init_app(app)  # This initializes the cache object for the app

    #app.register_blueprint(avis)
    #app.register_blueprint(avis_bp)    
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(agent_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(selection_bp)
    app.register_blueprint(zut)
    #app.register_blueprint(main_bp, name="main_bp", url_prefix="/")
    #app.register_blueprint(main_blueprint)
    #app.register_blueprint(main_blueprint, name="main_v1", url_prefix="/v1")
    #app.register_blueprint(main_blueprint, name="main_v2", url_prefix="/v2")
    #app.register_blueprint(dossier_blueprint)
    
    #app.register_blueprint(avis_bp, name="avis", url_prefix="/avis")
    
    app.register_blueprint(dossier, name="dossier", url_prefix="/")
    app.register_blueprint(control, name="control", url_prefix="/")
    app.register_blueprint(groupsel, name="groupsel", url_prefix="/")
    app.register_blueprint(book_list, name="book_list", url_prefix="/")
    app.register_blueprint(tree, name="tree", url_prefix="/")

    app.config['OUTPUT_DIR'] = 'app/static/generated_docs'

    return app

dotenv_path = join(dirname(__file__), '.env')  # Path to .env file
load_dotenv(dotenv_path)
FLASK_HOST=environ.get('FLASK_HOST')
FLASK_PORT=environ.get('FLASK_PORT')

app = create_app()
"""
if __name__ == "__main__":
    app.run(debug=True)
"""
if __name__ == "__main__":
    app.run(debug=True)
    print(f"Application disponible sur http://{FLASK_HOST}:{FLASK_PORT}")
    serve(app, host=FLASK_HOST, port=FLASK_PORT)