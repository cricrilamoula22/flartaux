from flask import Blueprint, render_template, request, jsonify, send_from_directory, current_app
from datetime import datetime
import os, threading, time
import pypyodbc
import traceback
from flask import send_file
from .config import Config
from app.utils.db import with_db_connection

from app.services.hfsql import (
    format_date_hfsql, get_main_records,
    get_sub_records, load_communes
)
#from app.services.generate_docs import generate_docx_and_zip
from app.services.generate_docs import generate_odt_and_zip
import pypyodbc
from datetime import datetime
from docx import Document
import zipfile
import io
from os import environ
#DSN = "DSN_ARTAUX"

main_bp = Blueprint('main', __name__)

HFSQL_HOST=environ.get('HFSQL_HOST')
HFSQL_PORT=environ.get('HFSQL_PORT')
HFSQL_DB=environ.get('HFSQL_DB')
HFSQL_USER=environ.get('HFSQL_USER')
HFSQL_PWD=environ.get('HFSQL_PWD')

DSN=f"DRIVER={{HFSQL}};Server Name={HFSQL_HOST};Server Port={HFSQL_PORT};Database={HFSQL_DB};UID={HFSQL_USER};  PWD={HFSQL_PWD}"
# dsn= "DSN=DSN_ARTAUX"
"""
@main_bp.route("/avis")
def index():
    return render_template("generate.html")
"""
@main_bp.route("/generate", methods=["POST"])
@with_db_connection
def generate(cursor):
    try:
        data = request.get_json()
        start_date = datetime.strptime(data['start_date'], "%Y-%m-%d")
        end_date = datetime.strptime(data['end_date'], "%Y-%m-%d")

        hf_start = format_date_hfsql(data['start_date'])
        hf_end = format_date_hfsql(data['end_date'])
        """
        conn = pypyodbc.connect(f"DSN={DSN}")
        cursor = conn.cursor()
        """
        conn = pypyodbc.connect(DSN)
        cursor = conn.cursor()

        communes = load_communes(cursor)
        main_records = get_main_records(hf_start, hf_end, cursor)

        sub_records = {
            rec["no_interne"]: get_sub_records(rec["no_interne"], hf_start, hf_end, cursor, communes)
            for rec in main_records
        }

        zip_path = generate_odt_and_zip(main_records, sub_records, start_date, end_date)

        # Nettoyage auto après 60 secondes
        def cleanup(paths):
            time.sleep(60)
            for p in paths:
                try:
                    os.remove(p)
                except:
                    pass

        all_files = [os.path.join(current_app.config['OUTPUT_DIR'], f"{r['no_interne']}.docx") for r in main_records]
        all_files.append(zip_path)
        threading.Thread(target=cleanup, args=(all_files,)).start()

        return jsonify({"status": "OK", "download_link": "/download_zip"})

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "trace": traceback.format_exc()
        }), 500

@main_bp.route('/download_zip')
def download_zip():
    zip_folder = os.path.join("static", "generated_docs")  # pas "app/static", car "static" est à la racine pour Flask
    zip_filename = "documents_fusionnes.zip"

    full_path = os.path.join("app", zip_folder, zip_filename)
    if not os.path.exists(full_path):
        print(f"[ERREUR] Fichier ZIP non trouvé : {full_path}")
        return "Fichier ZIP non trouvé", 404

    return send_from_directory(zip_folder, zip_filename, as_attachment=True)

@main_bp.route("/review", methods=["POST"])
@with_db_connection
def review(cursor):
    try:
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]

        hf_start = format_date_hfsql(start_date)
        hf_end = format_date_hfsql(end_date)

        conn = pypyodbc.connect(f"DSN={DSN}")
        cursor = conn.cursor()

        communes = load_communes(cursor)
        main_records = get_main_records(hf_start, hf_end, cursor)

        return render_template("template.html",
                               main_records=main_records,
                               start_date=start_date,
                               end_date=end_date,
                               download_link=None)  # Ne rien afficher encore
    except Exception as e:
        return f"Erreur lors du chargement : {str(e)}", 500


@main_bp.route("/generate_selected", methods=["POST"])
@with_db_connection
def generate_selected(cursor):
    try:
        from models import db, TreeCategories
        print("Version de generate_odt_and_zip importée :")
        print(generate_docs.generate_odt_and_zip)
        help(generate_docs.generate_odt_and_zip)

        categorie_7 = db.session.get(TreeCategories, 7)
        name_7 = categorie_7.name if categorie_7 else None          
        selected_ids = request.form.getlist("selected[]")
        print("Dossiers cochés :", selected_ids)

        """
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        """
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")

        if not start_date or not end_date:
            return "Les dates sont requises", 400


        hf_start = format_date_hfsql(start_date)
        hf_end = format_date_hfsql(end_date)

        conn = pypyodbc.connect(f"DSN={DSN}")
        cursor = conn.cursor()

        communes = load_communes(cursor)
        all_records = get_main_records(hf_start, hf_end, cursor)

        # Ne garder que les dossiers cochés
        #selected_records = [rec for rec in all_records if rec["no_interne"] in selected_ids]
        selected_records = []

        for rec in all_records:
            no_interne = rec["no_interne"]
            if no_interne not in selected_ids:
                continue

            # Lire les cases cochées dans le formulaire
            type_checked = f"type_checked_{no_interne}" in request.form
            motif_checked = f"motif_checked_{no_interne}" in request.form

            # Injecter ces valeurs dans le record pour qu'elles soient utilisées dans le template Jinja2
            rec["type_checked"] = type_checked
            rec["motif_checked"] = motif_checked

            selected_records.append(rec)

        # Charger les sous-enregistrements uniquement pour ceux sélectionnés
        sub_records = {
            rec["no_interne"]: get_sub_records(rec["no_interne"], hf_start, hf_end, cursor, communes)
            for rec in selected_records
        }

        zip_path = generate_odt_and_zip(
            selected_records,
            sub_records,
            datetime.strptime(start_date, "%Y-%m-%d"),
            datetime.strptime(end_date, "%Y-%m-%d"),
            name_7     # ← ajout IMPORTANT
        )


        return render_template("template.html",
                               main_records=selected_records,
                               start_date=start_date,
                               end_date=end_date,
                               download_link="/download_zip")
    except Exception as e:
        return f"Erreur : {e}<br><pre>{traceback.format_exc()}</pre>", 500
