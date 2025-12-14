from flask import Blueprint, render_template, request, jsonify, send_from_directory, current_app
from flask_login import login_required
from datetime import datetime
import os, threading, time, traceback
import pypyodbc

from .utils.db import with_db_connection
from .config import Config

from app.services.hfsql import (
    format_date_hfsql,
    get_main_records,
    get_sub_records,
    load_communes
)

from app.services.generate_docs import generate_odt_and_zip
from services.conditional_fusion import render_conditional_text

from models import db, TreeCategories, FusionTextBlock

# ------------------------------------------------------------------------------
# Configuration HFSQL
# ------------------------------------------------------------------------------
from os import environ

DSN = (
    f"DRIVER={{HFSQL}};"
    f"Server Name={environ.get('HFSQL_HOST')};"
    f"Server Port={environ.get('HFSQL_PORT')};"
    f"Database={environ.get('HFSQL_DB')};"
    f"UID={environ.get('HFSQL_USER')};"
    f"PWD={environ.get('HFSQL_PWD')}"
)

# ------------------------------------------------------------------------------
# Blueprint
# ------------------------------------------------------------------------------
main_bp = Blueprint("main", __name__, url_prefix="/avis")

# ------------------------------------------------------------------------------
# Page principale
# ------------------------------------------------------------------------------
@main_bp.route("/")
@login_required
def index():
    return render_template("generate.html")

# ------------------------------------------------------------------------------
# Aperçu HTML (sans génération ODT)
# ------------------------------------------------------------------------------
@main_bp.route("/review", methods=["POST"])
@with_db_connection
def review(cursor):
    try:
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]

        hf_start = format_date_hfsql(start_date)
        hf_end = format_date_hfsql(end_date)

        conn = pypyodbc.connect(DSN)
        cursor = conn.cursor()

        communes = load_communes(cursor)
        records = get_main_records(hf_start, hf_end, cursor)

        return render_template(
            "template.html",
            main_records=records,
            start_date=start_date,
            end_date=end_date,
            download_link=None
        )

    except Exception as e:
        return f"Erreur : {e}<pre>{traceback.format_exc()}</pre>", 500

# ------------------------------------------------------------------------------
# Génération ciblée avec fusion conditionnelle imbriquée
# ------------------------------------------------------------------------------
@main_bp.route("/generate_selected", methods=["POST"])
@with_db_connection
def generate_selected(cursor):
    try:
        # ----------------------------------------------------------------------
        # Chargement du bloc de fusion conditionnelle depuis la DB
        # ----------------------------------------------------------------------
        fusion_block = FusionTextBlock.query.filter_by(
            code="BLOC_TYPE_MOTIF"
        ).first()

        if not fusion_block:
            return "Bloc de fusion conditionnelle introuvable", 500

        # ----------------------------------------------------------------------
        # Catégories PostgreSQL (existant)
        # ----------------------------------------------------------------------
        cat_type = db.session.get(TreeCategories, 6)
        cat_motif = db.session.get(TreeCategories, 8)

        type_name = cat_type.name if cat_type else None
        motif_name = cat_motif.name if cat_motif else None

        # ----------------------------------------------------------------------
        # Paramètres formulaire
        # ----------------------------------------------------------------------
        selected_ids = request.form.getlist("selected[]")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")

        if not start_date or not end_date:
            return "Dates requises", 400

        hf_start = format_date_hfsql(start_date)
        hf_end = format_date_hfsql(end_date)

        # ----------------------------------------------------------------------
        # Chargement HFSQL
        # ----------------------------------------------------------------------
        conn = pypyodbc.connect(DSN)
        cursor = conn.cursor()

        communes = load_communes(cursor)
        all_records = get_main_records(hf_start, hf_end, cursor)

        selected_records = []

        for rec in all_records:
            if rec["no_interne"] not in selected_ids:
                continue

            # États des cases cochées
            rec["type_checked"] = f"type_checked_{rec['no_interne']}" in request.form
            rec["motif_checked"] = f"motif_checked_{rec['no_interne']}" in request.form

            rec["type_name"] = type_name if rec["type_checked"] else ""
            rec["motif_name"] = motif_name if rec["motif_checked"] else ""

            # ------------------------------------------------------------------
            # 🔐 Fusion conditionnelle sécurisée (DSL → texte final)
            # ------------------------------------------------------------------
            rec["fusion_blocs"] = render_conditional_text(
                fusion_block.template,
                rec
            )

            selected_records.append(rec)

        # ----------------------------------------------------------------------
        # Sous-enregistrements
        # ----------------------------------------------------------------------
        sub_records = {
            rec["no_interne"]: get_sub_records(
                rec["no_interne"], hf_start, hf_end, cursor, communes
            )
            for rec in selected_records
        }

        # ----------------------------------------------------------------------
        # Génération ODT + ZIP
        # ----------------------------------------------------------------------
        zip_path = generate_odt_and_zip(
            selected_records,
            sub_records,
            datetime.strptime(start_date, "%Y-%m-%d"),
            datetime.strptime(end_date, "%Y-%m-%d")
        )

        return render_template(
            "template.html",
            main_records=selected_records,
            start_date=start_date,
            end_date=end_date,
            download_link="/avis/download_zip"
        )

    except Exception as e:
        return f"Erreur : {e}<pre>{traceback.format_exc()}</pre>", 500

# ------------------------------------------------------------------------------
# Téléchargement ZIP
# ------------------------------------------------------------------------------
@main_bp.route("/download_zip")
def download_zip():
    zip_folder = os.path.join(
        current_app.root_path, "app", "static", "generated_docs"
    )
    zip_filename = "documents_fusionnes.zip"
    full_path = os.path.join(zip_folder, zip_filename)

    if not os.path.exists(full_path):
        return "Fichier ZIP introuvable", 404

    return send_from_directory(zip_folder, zip_filename, as_attachment=True)
