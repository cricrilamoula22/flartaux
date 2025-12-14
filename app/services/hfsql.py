from datetime import datetime
import re

# --- Dates ---
def parse_hfsql_date(val):
    try:
        if not val or str(val).strip() == '':
            return None
        return datetime.strptime(val, "%Y%m%d")
    except Exception as e:
        print(f"[parse_hfsql_date] Erreur: {e}")
        return None

def format_date_hfsql(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y%m%d")
    except Exception as e:
        print(f"[format_date_hfsql] Erreur: {e}")
        return ""

# --- Surface ---
def parse_surface(val):
    try:
        if val is None:
            return 0
        s = str(val).replace(' ', '').replace(',', '.').strip()
        return round(float(s) * 10000)
    except Exception as e:
        print(f"[parse_surface] Erreur: {e}")
        return 0

def format_superficie(m2):
    try:
        ha = m2 / 10000
        return f"{ha:.4f}".replace('.', ',') + " ha"
    except Exception as e:
        print(f"[format_superficie] Erreur: {e}")
        return "?"

# --- Parsing parcelle ---
import re

import re

import re

def transformer_parcelle(par_idsuf):
    try:
        # Code de la commune déléguée (positions 5 à 8)
        code_deleguee = par_idsuf[5:8]
        code_commune = code_deleguee if code_deleguee != "000" else ""

        # Section cadastrale (positions 8 à 10)
        section = par_idsuf[8:10].lstrip("0")

        # Numéro de parcelle + subdivision
        suffix = par_idsuf[10:]
        match = re.match(r"0*(\d+)([A-Z]*)", suffix)
        numero = match.group(1) if match else suffix
        subdivision = match.group(2) if match else ""

        return f"{code_commune}{section}{numero}{subdivision}"
    except Exception as e:
        print(f"[transformer_parcelle_affichage] Erreur avec '{par_idsuf}': {e}")
        return par_idsuf



# --- Chargement communes ---
def load_communes(cursor):
    try:
        cursor.execute("SELECT code_insee_commune, libelle_commune FROM t_commune")
        return {str(row[0]).strip(): row[1] for row in cursor.fetchall()}
    except Exception as e:
        print(f"[load_communes] Erreur: {e}")
        return {}

# --- Usagers ---
def get_nom_usager(cursor, pacage):
    cursor.execute(f"SELECT u_nom_raison_sociale FROM t_usager WHERE u_pacage = '{pacage}'")
    return (cursor.fetchone() or ["?"])[0]

def get_adresse_usager(cursor, pacage):
    cursor.execute(f"SELECT adr_postale_1, adr_postalcp FROM t_usadresse WHERE adr_pacage = '{pacage}'")
    addr = cursor.fetchone()
    return f"{addr[0]}\n{addr[1]}" if addr else "?"

# --- Requête principale ---
def get_main_records(date_debut, date_fin, cursor):
    query = f"""
SELECT no_interne, CAST(date_complet AS VARCHAR(10)) AS date_complet,
       no_pacage_demandeur, no_pacage_cedant,
       type_demande, motif_ctrl
FROM t_demande
WHERE date_complet BETWEEN '{date_debut}' AND '{date_fin}'
  AND date_complet <> ''
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    records = []
            
    for no_interne, date_complet, pac_dem, pac_ced, type_demande, motif_ctrl in rows:
        demandeur = get_nom_usager(cursor, pac_dem)
        adrdem = get_adresse_usager(cursor, pac_dem)
        cedant = get_nom_usager(cursor, pac_ced)

        records.append({
            "no_interne": no_interne,
            "date_complet": date_complet,
            "demandeur": demandeur,
            "adrdem": adrdem,
            "cedant": cedant,
            "type_demande": int(type_demande) if type_demande is not None else 0,
            "motif_ctrl": int(motif_ctrl) if motif_ctrl is not None else 0
        })

    return records

# --- Sous-enregistrements ---
def get_sub_records(no_interne, date_debut, date_fin, cursor, communes):
    sub = []

    # Ateliers
    cursor.execute(f"""
        SELECT d.code_insee, a.lib_atelier, d.nb_atelier, u.libunite
        FROM t_demande_batiment d
        JOIN t_type_atelier a ON d.id_atelier = a.idt_type_atelier
        JOIN t_unite u ON d.unite = u.idt_unite
        WHERE d.id_interne = '{no_interne}'
    """)
    for code_insee, atelier, nb, unite in cursor.fetchall():
        code = str(code_insee).strip()
        libelle = communes.get(code, "?")
        sub.append({
            "type": "ateliers",
            "libelles": libelle,
            "code_insee": code,
            "ateliers": atelier,
            "nb_atelier": nb,
            "libunite": unite
        })

    # Parcelles
    cursor.execute(f"""
        SELECT pd.par_idsuf, pd.par_surface
        FROM t_parceldem pd
        WHERE pd.par_nointerne = '{no_interne}'
    """)

    parcelles_by_commune = {}

    for par_idsuf, par_surface in cursor.fetchall():
        if not par_idsuf:
            continue

        insee_code = str(par_idsuf[:5]).strip()
        libelle = communes.get(insee_code, "?")
        parcelle_str = transformer_parcelle(par_idsuf)
        surface_val = parse_surface(par_surface)

        if libelle not in parcelles_by_commune:
            parcelles_by_commune[libelle] = {"parcelles": [], "surface_tot": 0}

        parcelles_by_commune[libelle]["parcelles"].append(parcelle_str)
        parcelles_by_commune[libelle]["surface_tot"] += surface_val

    for libelle, data in parcelles_by_commune.items():
        sub.append({
            "type": "parcelles",
            "libelles": libelle,
            "parcelles": " - ".join(data["parcelles"]),
            "superficie": format_superficie(data["surface_tot"])
        })

    return sub
