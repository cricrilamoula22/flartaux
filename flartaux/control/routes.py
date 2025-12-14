from flask import render_template
from flask import Flask, request, redirect, url_for, session, flash, jsonify, json
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import db
#from . import db
#from ..database import db
#from ..extensions import cache
#from ..parsel.models import TTParceldem
from models import TParceldem
from models import TDemande, TUsager
#from .models import TParceldem, TDemande
from sqlalchemy import case, func, distinct, cast, String
#from flask import current_app as app
from . import control
from sqlalchemy.orm import aliased

@control.route('/control')
@login_required
def pivot():
    #dossier_cible = 'C22250175'
    #no_interne = session.get('no_interne')
    dossier_cible = session.get('no_interne')

    # Étape 1 : Récupérer toutes les parcelles liées à ce dossier
    parcelles = db.session.query(distinct(TParceldem.par_idsuf)) \
        .filter(TParceldem.par_nointerne == dossier_cible).all()
    parcelle_ids = [p[0] for p in parcelles]

    # Étape 2 : Trouver tous les dossiers qui partagent ces parcelles
    keys = db.session.query(distinct(TParceldem.par_nointerne)) \
        .filter(TParceldem.par_idsuf.in_(parcelle_ids)).all()
    key_values = [k[0] for k in keys]
    
    UsagerDemandeur = aliased(TUsager)
    UsagerCedant = aliased(TUsager)

    columns = [TParceldem.par_idsuf, TParceldem.par_surface]

    for key in key_values:
        col = func.max(
            case(
                (TParceldem.par_nointerne == key,
                TParceldem.par_idsuf + ' / ' +
                cast(TParceldem.par_surface, String) + ' / ' +
                TDemande.no_pacage_demandeur + ' / ' +
                UsagerDemandeur.u_nom_raison_sociale + ' / ' +
                UsagerCedant.u_nom_raison_sociale)
            )
        ).label(f'col_{key}')
        columns.append(col)

    query = db.session.query(*columns) \
        .join(TDemande, TDemande.no_interne == TParceldem.par_nointerne) \
        .join(UsagerDemandeur, UsagerDemandeur.u_pacage == TDemande.no_pacage_demandeur) \
        .join(UsagerCedant, UsagerCedant.u_pacage == TDemande.no_pacage_cedant) \
        .filter(TParceldem.par_idsuf.in_(parcelle_ids)) \
        .group_by(TParceldem.par_idsuf, TParceldem.par_surface)

    data = [dict(row._mapping) for row in query]

    """
    # Étape 3 : Construire les colonnes dynamiques
    columns = [TParceldem.par_idsuf, TParceldem.par_surface]
    for key in key_values:
        col = func.max(
            case(
                (TParceldem.par_nointerne == key,
                TParceldem.par_idsuf + ' / ' +
                cast(TParceldem.par_surface, String) + ' / ' +
                TDemande.no_pacage_demandeur + ' / ' +
                TParceldem.par_nointerne + ' / ' +
                TUsager.u_nom_raison_sociale)
            )
        ).label(f'col_{key}')

        columns.append(col)

    # Étape 4 : Requête pivot
    query = db.session.query(*columns) \
        .join(TDemande, TDemande.no_interne == TParceldem.par_nointerne) \
        .join(TUsager, TUsager.u_pacage == TDemande.no_pacage_demandeur) \
        .filter(TParceldem.par_idsuf.in_(parcelle_ids)) \
        .group_by(TParceldem.par_idsuf, TParceldem.par_surface)

    data = [dict(row._mapping) for row in query]

    demandeurs = db.session.query(
        TDemande.no_interne,
        TUsager.u_nom_raison_sociale
    ).join(
        TUsager, TDemande.no_pacage_demandeur == TUsager.u_pacage
    ).filter(
        TDemande.no_interne.in_(key_values)
    ).all()

    labels = {no_interne: nom for no_interne, nom in demandeurs}
    """
    # Dictionnaires de labels pour affichage
    labels = {
        d.no_interne: {
            "demandeur": dd_nom,
            "cedant": cd_nom
        }
        for d, dd_nom, cd_nom in db.session.query(
            TDemande,
            UsagerDemandeur.u_nom_raison_sociale,
            UsagerCedant.u_nom_raison_sociale
        )
        .join(UsagerDemandeur, UsagerDemandeur.u_pacage == TDemande.no_pacage_demandeur)
        .join(UsagerCedant, UsagerCedant.u_pacage == TDemande.no_pacage_cedant)
        .filter(TDemande.no_interne.in_(key_values))
        .all()
    }

    """
    labels = {}

    for key in key_values:
        demande = db.session.query(TUsager.u_nom_raison_sociale) \
            .filter(TDemande.no_interne == key).first()
        labels[key] = demande[0] if demande else "Inconnu"
    """
    """
    return render_template('pivot.html',
                       data=data,
                       keys=key_values,
                       labels=labels,
                       cooccurrence_map=cooccurrence_map,
                       nb_partagees=nb_partagees)
    """
    return render_template('pivot.html', data=data, keys=key_values, labels=labels)
