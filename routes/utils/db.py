# app/utils/db.py
import pypyodbc
from functools import wraps
from flask import jsonify
import traceback

from datetime import datetime
from docx import Document
import zipfile
import io
from os import environ

HFSQL_HOST=environ.get('HFSQL_HOST')
HFSQL_PORT=environ.get('HFSQL_PORT')
HFSQL_DB=environ.get('HFSQL_DB')
HFSQL_USER=environ.get('HFSQL_USER')
HFSQL_PWD=environ.get('HFSQL_PWD')

DSN=f"DRIVER={{HFSQL}};Server Name={HFSQL_HOST};Server Port={HFSQL_PORT};Database={HFSQL_DB};UID={HFSQL_USER};  PWD={HFSQL_PWD}"

#DSN = "DSN_ARTAUX"
def with_db_connection(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        conn = None
        try:
            conn = pypyodbc.connect(DSN)
            #conn = pypyodbc.connect(f"DSN={DSN}")
            cursor = conn.cursor()
            return view_func(cursor, *args, **kwargs)
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e),
                "trace": traceback.format_exc()
            }), 500
        finally:
            if conn:
                try:
                    conn.close()
                except Exception as close_err:
                    print(f"[WARN] Erreur lors de la fermeture de la connexion :{close_err}")
    return wrapped_view