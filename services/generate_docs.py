import os
import zipfile
import pprint
import html
import unicodedata
import xml.etree.ElementTree as ET
import re
from python_odt_template import ODTTemplate
from python_odt_template.jinja import get_odt_renderer
from models import db, TreeCategories
# =========================
# 📁 Chemins de base
# =========================
TEMPLATE_PATH = "app/templates/template.odt"
OUTPUT_DIR = "app/static/generated_docs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# =========================
# ✅ Validation XML
# =========================
def is_valid_xml_char(c):
    """
    Retourne True si le caractère est autorisé en XML 1.0.
    Les plages étendues sont nécessaires pour supporter tous les caractères UTF-8.
    """
    codepoint = ord(c)
    # 0x9 (TAB), 0xA (LF), 0xD (CR)
    # Plages régulières (0x20 à 0xD7FF)
    # Plages privées et étendues (0xE000 à 0xFFFD et au-delà de 0x10000)
    return (
        codepoint == 0x9
        or codepoint == 0xA
        or codepoint == 0xD
        or (0x20 <= codepoint <= 0xD7FF)
        or (0xE000 <= codepoint <= 0xFFFD)
        or (0x10000 <= codepoint <= 0x10FFFF)
    )


# =========================
# 🧼 Nettoyage des chaînes
# =========================
def clean_and_escape(value):
    """Nettoie et échappe une valeur pour garantir une insertion XML UTF-8 sûre."""
    if not isinstance(value, str):
        return value

    # --- Étape 1: Élimination BRUTALE des caractères de contrôle non XML valides ---
    # Ceci est essentiel pour corriger l'erreur 'invalid token' et assurer la fusion.
    # Regex pour les caractères ASCII 0x00-0x08, 0x0B, 0x0C, 0x0E-0x1F.
    control_chars = re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F]')
    value = control_chars.sub('', value)
    
    # --- Étape 2: Remplacement des accents par des lettres sans accent ---
    
    # Remplacement du caractère de remplacement U+FFFD () par "??".
    value = value.replace('\ufffd', '??') 

    # Normalisation Unicode pour décomposer les caractères accentués (ex: 'é' -> 'e' + accent)
    # Puis on retire les marques diacritiques.
    try:
        normalized_value = unicodedata.normalize('NFD', value)
        # Filtre pour ne garder que les caractères de base (lettres non accentuées, chiffres, ponctuation)
        value = ''.join(c for c in normalized_value if unicodedata.category(c) != 'Mn')
    except Exception as e:
        # En cas d'échec, on logue et on continue avec la valeur non traitée.
        print(f"Erreur lors de la suppression des accents: {e}")
        
    # --- Étape 3: Finalisation XML ---

    # Normalisation Unicode (gardée par principe)
    value = unicodedata.normalize("NFC", value)

    # Suppression des caractères interdits XML (ceux qui sont en dehors des plages autorisées)
    value = "".join(c for c in value if is_valid_xml_char(c))

    # Échappement HTML des caractères spéciaux (& < >)
    value = html.escape(value, quote=False)

    # Uniformisation des retours à la ligne
    value = value.replace("\r\n", "\n").replace("\r", "\n")

    return value


def sanitize_context(context):
    """Applique le nettoyage à tout le dictionnaire de rendu."""
    def clean_dict(d):
        cleaned = {}
        for k, v in d.items():
            new_v = clean_and_escape(v)
            if isinstance(v, str) and v != new_v:
                # Affichage des corrections si elles ont eu lieu (utile pour le debug)
                # Utiliser repr() permet de voir les caractères invisibles comme '\n' ou '\x00'
                print(f"[✔️ Nettoyé] champ '{k}' : {repr(v)[:50]}... → {repr(new_v)[:50]}...")
            cleaned[k] = new_v
        return cleaned

    # Correction: On s'assure que les champs des dates sont aussi nettoyés si nécessaire
    context["start_date"] = clean_and_escape(context.get("start_date", ""))
    context["end_date"] = clean_and_escape(context.get("end_date", ""))

    context["main_record"] = clean_dict(context["main_record"])
    context["sub_records"] = [clean_dict(sub) for sub in context["sub_records"]]
    return context


# =========================
# 🔍 Contrôle des caractères interdits
# =========================
def scan_for_invalid_chars(text, label):
    """Affiche les caractères interdits (rare, mais utile en debug)."""
    for i, c in enumerate(text):
        if not is_valid_xml_char(c):
            print(
                f"[❌ Caractère interdit] {label} — pos {i} — {repr(c)} — code {ord(c)}"
            )


# =========================
# 🧩 Vérification du fichier .odt
# =========================
def is_odt_valid(odt_path):
    """Retourne True si le fichier ODT est bien formé, sinon le message d’erreur."""
    try:
        with zipfile.ZipFile(odt_path, "r") as odt_zip:
            with odt_zip.open("content.xml") as content_file:
                ET.parse(content_file)
        return True
    except Exception as e:
        return str(e)

def get_name_cat_hfsql(id_sous_priorite=12):
    """Récupère le lib_sous_priorite depuis HFSQL via ODBC."""
    conn_str = r"Driver=HFSQL ODBC;Server=MONSERVEUR;Database=MA_BASE;Uid=monuser;Pwd=monmdp;"
    try:
        conn = pypyodbc.connect(conn_str)
        cursor = conn.cursor()
        query = "SELECT lib_sous_priorite FROM t_sous_priorite WHERE idt_sous_priorite = ?"
        cursor.execute(query, (id_sous_priorite,))
        row = cursor.fetchone()
        return row[0] if row else None
    except Exception as e:
        print(f"⚠️ Erreur HFSQL : {e}")
        return None
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass
# =========================
# 🧠 Fusion & génération
# =========================
def generate_odt_and_zip(main_records, sub_records, start_date, end_date):
    """
    Fusionne les dossiers principaux et sous-enregistrements,
    génère les fichiers ODT et crée un ZIP final.
    """
    generated_files = []
    corrupted_files = []
    renderer = get_odt_renderer(media_path="media/")

    for record in main_records:
        no_interne = record["no_interne"]
        current_sub_records = sub_records.get(no_interne, [])
        print(f"\n📄 Fusion du dossier {no_interne} avec {len(current_sub_records)} sous-enregistrements")

        # ✅ Contexte avec séparation HFSQL / PostgreSQL
        context = {
            "main_record": record,  # Contient déjà type_name et motif_name
            "sub_records": current_sub_records,
            "start_date": start_date.strftime("%d/%m/%Y"),
            "end_date": end_date.strftime("%d/%m/%Y"),
            "page_break": "\n---PAGEBREAK---\n",
        }

        temp_path = os.path.join(OUTPUT_DIR, f"{no_interne}.odt")
        pprint.pprint(context)

        with ODTTemplate(TEMPLATE_PATH) as template:
            sanitized = sanitize_context(context)

            # Vérification manuelle (facultative)
            for k, v in sanitized["main_record"].items():
                if isinstance(v, str):
                    scan_for_invalid_chars(v, f"{no_interne}:{k}")
            for sub in sanitized["sub_records"]:
                for k, v in sub.items():
                    if isinstance(v, str):
                        scan_for_invalid_chars(v, f"{no_interne}:{k}")

            rendered = renderer.render(template, sanitized)
            template.pack(temp_path)

        # Validation XML
        validation = is_odt_valid(temp_path)
        if validation is True:
            print(f"✅ Fichier généré et valide : {temp_path}")
            generated_files.append(temp_path)
        else:
            print(f"❌ Fichier corrompu : {temp_path}\n    Erreur : {validation}")
            corrupted_files.append((temp_path, validation))

    # Création du ZIP final
    zip_path = os.path.join(OUTPUT_DIR, "documents_fusionnes.zip")
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for f in generated_files:
            zipf.write(f, os.path.basename(f))

    print(f"\n✅ {len(generated_files)} fichiers valides ajoutés au ZIP.")
    if corrupted_files:
        print(f"⚠️ {len(corrupted_files)} fichiers corrompus détectés.")

    return zip_path
