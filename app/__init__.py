from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Configuration globale ici si besoin
    app.config['OUTPUT_DIR'] = 'app/static/generated_docs'

    # Import du blueprint principal
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
