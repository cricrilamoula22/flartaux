from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import date
from typing import List, Optional
from sqlalchemy import (
    Integer, String, Text, Numeric, Date, UniqueConstraint,
    ForeignKey, Table, Column, text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional

from sqlalchemy import BigInteger, Boolean, CheckConstraint, Column, Date, DateTime, ForeignKeyConstraint, Index, Integer, Numeric, PrimaryKeyConstraint, String, Text, UniqueConstraint, text
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped


from sqlalchemy import (
    Column, Integer, String, ForeignKeyConstraint,
    PrimaryKeyConstraint, UniqueConstraint
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from extensions import db

SCHEMA = "w_sadr_artaux"

from models import db
from sqlalchemy import Table, Column, Integer, Float, Text, Date, Boolean, String, ForeignKey
from sqlalchemy import create_engine, Column, Integer, BigInteger, Text, Date, Boolean, String, MetaData, Table
from sqlalchemy import PrimaryKeyConstraint, Index, UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.orm import relationship, foreign
from sqlalchemy.sql import and_
'''
class TCadastre(db.Model):
    __tablename__ = 't_cadastre'
    __table_args__ = {'schema': SCHEMA}
    idt_cadastre = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idsuf = db.Column(db.String(18), db.ForeignKey('t_parceldem.par_idsuf'), unique=True, nullable=False)
    idpar = db.Column(db.String(18))
    idprocpte = db.Column(db.String(17))
    idcom = db.Column(db.String(6), db.ForeignKey('t_commune.code_insee_commune'))
    ccosec = db.Column(db.String(3))
    dnupla = db.Column(db.String(5))
    ccosub = db.Column(db.String(3))
    dcntsf = db.Column(db.BigInteger)
    idprocpte_org = db.Column(db.Text)

    # Relationships
    t_parceldem = db.relationship('TParceldem', back_populates='t_cadastre')
    commune = db.relationship('TCommune', back_populates='cadastres')
    selections = db.relationship('SelectionParcelle', back_populates='cadastre')

class TCadastre(db.Model):
    __tablename__ = 't_cadastre'
    __table_args__ = {'schema': SCHEMA}

    idt_cadastre = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # ❌ do not reference t_parceldem
    idsuf = db.Column(db.String(18), unique=True, nullable=False)

    idpar = db.Column(db.String(18))
    idprocpte = db.Column(db.String(17))
    idcom = db.Column(db.String(6), db.ForeignKey(f"{SCHEMA}.t_commune.code_insee_commune"))
    dnupla = db.Column(db.String(5))
    ccosub = db.Column(db.String(3))
    dcntsf = db.Column(db.BigInteger)
    idprocpte_org = db.Column(db.Text)
    
    t_parceldem = db.relationship('TParceldem', back_populates='t_cadastre')
'''    

class FusionTextBlock(db.Model):
    __tablename__ = "fusion_text_blocks"
    __table_args__ = {'schema': SCHEMA}
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    template = db.Column(db.Text, nullable=False)


class TCadastre(db.Model):
    __tablename__ = 't_cadastre'
    __table_args__ = {'schema': SCHEMA}

    idt_cadastre = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idsuf = db.Column(db.String(18), unique=True, nullable=False)
    idpar = db.Column(db.String(18))
    idprocpte = db.Column(db.String(17))
    idcom = db.Column(db.String(6), db.ForeignKey(f"{SCHEMA}.t_commune.code_insee_commune"))
    ccosec = db.Column(db.String(3))
    dnupla = db.Column(db.String(5))
    ccosub = db.Column(db.String(3))
    dcntsf = db.Column(db.BigInteger)
    idprocpte_org = db.Column(db.Text)

    # Relationships
    t_parceldem = db.relationship('TParceldem', back_populates='t_cadastre')

    commune = db.relationship('TCommune', back_populates='cadastres')

    selections = db.relationship(
        'SelectionParcelle',
        back_populates='cadastre',
        cascade="all, delete-orphan"
    )

'''
class SelectionParcelle(db.Model):
    __tablename__ = 'selection_parcelle'
    __table_args__ = {'schema': SCHEMA}
    session_id = db.Column(db.String(128), primary_key=True)
    idsuf = db.Column(db.String(20), db.ForeignKey('t_cadastre.idsuf'), primary_key=True)
    surface_demandee = db.Column(db.BigInteger, nullable=False)

    # Relationship to t_cadastre
    cadastre = db.relationship('TCadastre', back_populates='selections')

class SelectionParcelle(db.Model):
    __tablename__ = 'selection_parcelle'
    __table_args__ = {'schema': SCHEMA}

    session_id = db.Column(db.String(128), primary_key=True)

    idsuf = db.Column(
        db.String(20),
        db.ForeignKey(f"{SCHEMA}.t_cadastre.idsuf"),
        primary_key=True
    )

    surface_demandee = db.Column(db.BigInteger, nullable=False)

    cadastre = db.relationship('TCadastre', back_populates='selections')
'''
class SelectionParcelle(db.Model):
    __tablename__ = 'selection_parcelle'
    __table_args__ = {'schema': SCHEMA}

    session_id = db.Column(db.String(128), primary_key=True)
    idsuf = db.Column(
        db.String(20),
        db.ForeignKey(f"{SCHEMA}.t_cadastre.idsuf"),
        primary_key=True
    )
    surface_demandee = db.Column(db.BigInteger, nullable=False)

    cadastre = db.relationship("TCadastre", back_populates='selections')


class TCommune(db.Model):
    __tablename__ = 't_commune'
    __table_args__ = {'schema': SCHEMA}
    idt_commune = db.Column(db.Integer, primary_key=True, autoincrement=True)
    '''
    com = db.Column(db.String(6), unique=True)
    dep = db.Column(db.String(3))
    can = db.Column(db.String(5))
    libelle = db.Column(db.String(255))
    '''
    code_insee_commune = mapped_column(String(5), server_default=text('NULL::character varying'))
    code_dep = mapped_column(String(3), server_default=text('NULL::character varying'))
    code_canton = mapped_column(String(4), server_default=text('NULL::character varying'))
    libelle_commune = mapped_column(String(74), server_default=text('NULL::character varying'))


    # Relationship to t_cadastre
    cadastres = db.relationship('TCadastre', back_populates='commune')
    
'''
class SelectionParcelle(db.Model):
    __tablename__ = 'selection_parcelle'
    __table_args__ = {'schema': SCHEMA}    

    session_id = mapped_column(db.String(128), primary_key=True)
    idsuf = mapped_column(String(20), db.ForeignKey('t_cadastre.idsuf'), primary_key=True)
    surface_demandee = mapped_column(BigInteger, nullable=False)

    # Relationship to t_cadastre
    #cadastre = db.relationship('TCadastre', back_populates='selections')

    cadastre: Mapped[List['TCadastre']] = relationship('TCadastre', back_populates='selections')
'''

class TCadDem(db.Model):
    __tablename__ = 't_cad_dem'
    __table_args__ = {'schema': SCHEMA}
    __table_args__ = (
        PrimaryKeyConstraint('idt_cad_dem', name='t_cad_dem_pkey'),
        Index('idx_t_cad_dem_idprocpte', 'idprocpte'),
        Index('idx_t_cad_dem_idsuf', 'idsuf')
    )

    idt_cad_dem = mapped_column(BigInteger)
    idsuf = mapped_column(String(17), server_default=text('NULL::character varying'))
    idpar = mapped_column(String(17), server_default=text('NULL::character varying'))
    idprocpte = mapped_column(String(22), server_default=text('NULL::character varying'))
    idcom = mapped_column(String(6), server_default=text('NULL::character varying'))
    ccosec = mapped_column(String(3), server_default=text('NULL::character varying'))
    dnupla = mapped_column(String(5), server_default=text('NULL::character varying'))
    ccosub = mapped_column(String(3), server_default=text('NULL::character varying'))
    dcntsf = mapped_column(BigInteger)
    idprocpte_org = mapped_column(Text)

'''
class TCadastre(db.Model):
    __tablename__ = 't_cadastre'
    __table_args__ = {'schema': SCHEMA}
    __table_args__ = (
        PrimaryKeyConstraint('idt_cadastre', name='t_cadastre_pkey'),
        UniqueConstraint('idsuf', name='unique_idsuf'),
        Index('idx_t_cadastre_idprocpte', 'idprocpte'),
        Index('idx_t_cadastre_idsuf', 'idsuf')
    )

    idt_cadastre = mapped_column(BigInteger)
    idsuf = mapped_column(String(17), server_default=text('NULL::character varying'))
    idpar = mapped_column(String(17), server_default=text('NULL::character varying'))
    idprocpte = mapped_column(String(22), server_default=text('NULL::character varying'))
    idcom = mapped_column(String(6), server_default=text('NULL::character varying'))
    ccosec = mapped_column(String(3), server_default=text('NULL::character varying'))
    dnupla = mapped_column(String(5), server_default=text('NULL::character varying'))
    ccosub = mapped_column(String(3), server_default=text('NULL::character varying'))
    dcntsf = mapped_column(BigInteger)
    idprocpte_org = mapped_column(Text)

    t_parceldem: Mapped[List['TParceldem']] = relationship('TParceldem', uselist=True, back_populates='t_cadastre')
    # Relationships
    commune: Mapped[List['TCommune']] = relationship('TCommune', back_populates='cadastres')
    selections: Mapped[List['SelectionParcelle']] = relationship('SelectionParcelle', back_populates='cadastre')

class TCadastre(db.Model):
    __tablename__ = 't_cadastre'

    idt_cadastre = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idsuf = db.Column(db.String(18), unique=True, nullable=False)
    idpar = db.Column(db.String(18))
    idprocpte = db.Column(db.String(17))
    idcom = db.Column(db.String(6), db.ForeignKey('t_commune.com'))
    ccosec = db.Column(db.String(3))
    dnupla = db.Column(db.String(5))
    ccosub = db.Column(db.String(3))
    dcntsf = db.Column(db.BigInteger)
    idprocpte_org = db.Column(db.Text)

    # Relationships
    commune = db.relationship('TCommune', back_populates='cadastres')
'''
class TCom2023(db.Model):
    __tablename__ = 't_com2023'
    __table_args__ = {'schema': SCHEMA}
    __table_args__ = (
        PrimaryKeyConstraint('idt_com2023', name='t_com2023_pkey'),
    )

    idt_com2023 = mapped_column(BigInteger)
    com = mapped_column(String(6), server_default=text('NULL::character varying'))
    dep = mapped_column(String(3), server_default=text('NULL::character varying'))
    can = mapped_column(String(5), server_default=text('NULL::character varying'))
    libelle = mapped_column(String(255), server_default=text('NULL::character varying'))

'''
class TCommune(db.Model):
    __tablename__ = 't_commune'
    __table_args__ = {'schema': SCHEMA}
    __table_args__ = (
        PrimaryKeyConstraint('idt_commune', name='t_commune_pkey'),
    )

    idt_commune = mapped_column(BigInteger)
    code_insee_commune = mapped_column(String(5), server_default=text('NULL::character varying'))
    code_dep = mapped_column(String(3), server_default=text('NULL::character varying'))
    code_canton = mapped_column(String(4), server_default=text('NULL::character varying'))
    libelle_commune = mapped_column(String(74), server_default=text('NULL::character varying'))

class TCommune(db.Model):
    __tablename__ = 't_commune'
    __table_args__ = {'schema': SCHEMA}
    __table_args__ = (
        PrimaryKeyConstraint('idt_commune', name='t_commune_pkey'),
    )
    idt_commune = db.Column(db.Integer, primary_key=True, autoincrement=True)
    com = mapped_column(String(6), unique=True)
    dep = mapped_column(String(3))
    can = mapped_column(String(5))
    libelle = mapped_column(String(255))

    # Relationship to t_cadastre
    #cadastres = db.relationship('TCadastre', back_populates='commune')
    commune: Mapped[List['TCadastre']] = relationship('TCadastre', back_populates='cadastres')    
'''
class TDemande(db.Model):
    __tablename__ = 't_demande'
    __table_args__ = {'schema': SCHEMA}
    __table_args__ = (
        PrimaryKeyConstraint('idt_demande', name='t_demande_pkey'),
    )

    idt_demande = mapped_column(BigInteger)
    no_interne = mapped_column(String(36), server_default=text('NULL::character varying'))
    date_de_depot = mapped_column(Date)
    date_complet = mapped_column(Date)
    code_avis = mapped_column(String(1), server_default=text('NULL::character varying'))
    id_commission = mapped_column(Integer)
    date_limiteval = mapped_column(Date)
    no_pacage_demandeur = mapped_column(String(9), server_default=text('NULL::character varying'))
    dem_autprof = mapped_column(String(30), server_default=text('NULL::character varying'))
    no_pacage_cedant = mapped_column(String(9), server_default=text('NULL::character varying'))
    jeune_agriculteur = mapped_column(Integer)
    jeune_agr_aide = mapped_column(Integer)
    code_motifcess = mapped_column(Integer)
    type_demande = mapped_column(Integer)
    cedantinforme = mapped_column(Integer)
    uta_demandeur = mapped_column(String(50), server_default=text('NULL::character varying'))
    nb_salaries = mapped_column(String(50), server_default=text('NULL::character varying'))
    sau_demandeur = mapped_column(String(50), server_default=text('NULL::character varying'))
    smi = mapped_column(String(2), server_default=text('NULL::character varying'))
    demanter = mapped_column(Integer)
    surface_demandee = mapped_column(String(50), server_default=text('NULL::character varying'))
    distance_siege = mapped_column(String(50), server_default=text('NULL::character varying'))
    distance_parcelle = mapped_column(String(50), server_default=text('NULL::character varying'))
    surface_unite_ref = mapped_column(String(50), server_default=text('NULL::character varying'))
    date_transfert = mapped_column(Date)
    demanhs = mapped_column(Integer)
    type_demande_hs = mapped_column(Integer)
    natu_demande_hs = mapped_column(Integer)
    effectifhs = mapped_column(Integer)
    sau_ponderee_demandeur = mapped_column(String(50), server_default=text('NULL::character varying'))
    pad_demandeur = mapped_column(String(50), server_default=text('NULL::character varying'))
    date_signature_decision = mapped_column(Date)
    motif_ctrl = mapped_column(String(2), server_default=text('NULL::character varying'))
    code_decision = mapped_column(String(1), server_default=text('NULL::character varying'))
    date_editdecis = mapped_column(Date)
    optimclecomp_no_pa_id_co = mapped_column(String(13), server_default=text('NULL::character varying'))
    sau_cedant = mapped_column(String(50), server_default=text('NULL::character varying'))
    date_avis = mapped_column(Date)
    code_statut = mapped_column(String(1), server_default=text('NULL::character varying'))
    motiv_c = mapped_column(Text)
    motiv_d = mapped_column(Text)
    motiv_a = mapped_column(Text)
    motiv_p = mapped_column(Text)
    sele_motictrl = mapped_column(Integer)
    id_commissioncode_statut = mapped_column(String(4), server_default=text('NULL::character varying'))
    no_pacage_demandeurid_commission = mapped_column(String(15), server_default=text('NULL::character varying'))
    no_pacage_cedantno_interne = mapped_column(String(20), server_default=text('NULL::character varying'))
    id_commissioncode_statutno_pacage_cedant = mapped_column(String(15), server_default=text('NULL::character varying'))
    aj6mois = mapped_column(String(1), server_default=text('NULL::character varying'))
    env_giee = mapped_column(Boolean)
    env_dephy = mapped_column(Boolean)
    env_cert_maaf = mapped_column(Boolean)
    env_cert_biopart = mapped_column(Boolean)
    env_cert_biotot = mapped_column(Boolean)
    distance_siege_proche = mapped_column(String(50), server_default=text('NULL::character varying'))
    distance_siege_eloigne = mapped_column(String(50), server_default=text('NULL::character varying'))
    rt_compens_utilpub = mapped_column(Boolean)
    rt_compens_utilpub_surf = mapped_column(String(50), server_default=text('NULL::character varying'))
    rt_compens_rprop = mapped_column(Boolean)
    rt_compens_rprop_surf = mapped_column(Integer)
    rt_compens_autre = mapped_column(Boolean)
    rt_compens_autre_surf = mapped_column(String(50), server_default=text('NULL::character varying'))
    rt_compens_autre_motif = mapped_column(String(50), server_default=text('NULL::character varying'))
    rt_deplanimaux = mapped_column(Boolean)
    rt_deplanimaux_surf = mapped_column(String(50), server_default=text('NULL::character varying'))
    rt_echcedant = mapped_column(Boolean)
    rt_echcedant_surf = mapped_column(String(50), server_default=text('NULL::character varying'))
    rt_bio = mapped_column(Boolean)
    rt_bio_surf = mapped_column(String(50), server_default=text('NULL::character varying'))
    surf_rep_bio = mapped_column(String(50), server_default=text('NULL::character varying'))
    surf_rep_echange = mapped_column(String(50), server_default=text('NULL::character varying'))
    surf_rep_depanimaux = mapped_column(Integer)
    reprise_dossier = mapped_column(Boolean)
    date_limite_depot = mapped_column(Date)
    nb_concurrences = mapped_column(Integer)
    env_titre_sec = mapped_column(Boolean)
    id_naturetransac = mapped_column(Integer)
    instal3p = mapped_column(Integer)
    instalstage = mapped_column(Integer)
    instaletude = mapped_column(Integer)
    cedantexpab = mapped_column(Integer)
    cedantexpconv = mapped_column(Integer)
    rt_compens_ind_surf = mapped_column(Boolean)
    ide_globale = mapped_column(String(50), server_default=text('NULL::character varying'))
    surf_zsce = mapped_column(String(50), server_default=text('NULL::character varying'))
    id_redaction_decision = mapped_column(Integer)
    total_ide = mapped_column(String(50), server_default=text('NULL::character varying'))
    id_gestionnaire = mapped_column(Integer)
    demandebat = mapped_column(Integer)
    saup = mapped_column(String(50), server_default=text('NULL::character varying'))
    dossiersuccessif = mapped_column(Boolean)
    dossierconcurrentsuccessif = mapped_column(Boolean)
    ideuta = mapped_column(String(50), server_default=text('NULL::character varying'))
    memodemandeur = mapped_column(Text)
    memocedant = mapped_column(Text)
    recours = mapped_column(Boolean)
    daterecours = mapped_column(Date)
    id_logics = mapped_column(String(50), server_default=text('NULL::character varying'))
    pideuta = mapped_column(String(50), server_default=text('NULL::character varying'))
    schema = mapped_column(Integer)
    sempastous = mapped_column(Boolean)
    date_sempastous = mapped_column(Date)
    user_id = mapped_column(String(36))
    

class TDemandeBatiment(db.Model):
    __tablename__ = 't_demande_batiment'
    __table_args__ = {'schema': SCHEMA}
    __table_args__ = (
        PrimaryKeyConstraint('id', name='t_demande_batiment_pkey'),
    )

    id = mapped_column(BigInteger)
    idt_demande_batiment = mapped_column(BigInteger)
    id_interne = mapped_column(String(9), server_default=text('NULL::character varying'))
    id_atelier = mapped_column(BigInteger)
    nb_atelier = mapped_column(String(20), server_default=text('NULL::character varying'))
    code_insee = mapped_column(String(5), server_default=text('NULL::character varying'))
    unite = mapped_column(BigInteger)
    indiceatelier = mapped_column(BigInteger)
    idsuf = mapped_column(String(17), server_default=text('NULL::character varying'))


class TMvtcommune(db.Model):
    __tablename__ = 't_mvtcommune'
    __table_args__ = {'schema': SCHEMA}
    __table_args__ = (
        PrimaryKeyConstraint('idt_mvtcommune', name='t_mvtcommune_pkey'),
    )

    idt_mvtcommune = mapped_column(BigInteger)
    mod = mapped_column(Integer)
    dateeff = mapped_column(Date)
    typecomav = mapped_column(String(4), server_default=text('NULL::character varying'))
    comav = mapped_column(String(5), server_default=text('NULL::character varying'))
    tnccav = mapped_column(Integer)
    nccav = mapped_column(String(255), server_default=text('NULL::character varying'))
    nccenrav = mapped_column(String(255), server_default=text('NULL::character varying'))
    libelleav = mapped_column(String(255), server_default=text('NULL::character varying'))
    typecomap = mapped_column(String(4), server_default=text('NULL::character varying'))
    comap = mapped_column(String(5), server_default=text('NULL::character varying'))
    tnccap = mapped_column(Integer)
    nccap = mapped_column(String(255), server_default=text('NULL::character varying'))
    nccenrap = mapped_column(String(255), server_default=text('NULL::character varying'))
    libelleap = mapped_column(String(255), server_default=text('NULL::character varying'))


class TParcelStatut(db.Model):
    __tablename__ = 't_parcel_statut'
    __table_args__ = {'schema': SCHEMA}
    __table_args__ = (
        PrimaryKeyConstraint('idt_parcel_statut', name='t_parcel_statut_pkey'),
    )

    idt_parcel_statut = mapped_column(BigInteger)
    id_parcel_statut = mapped_column(String(17), server_default=text('NULL::character varying'))
    par_idsuf = mapped_column(String(17), server_default=text('NULL::character varying'))
    no_interne = mapped_column(String(9), server_default=text('NULL::character varying'))
    no_interne_pub = mapped_column(String(9), server_default=text('NULL::character varying'))
    date_pub_pref = mapped_column(Date)
    date_pub_mairie = mapped_column(Date)
    date_limite_concu = mapped_column(Date)
    par_idsufno_interne = mapped_column(String(255), server_default=text('NULL::character varying'))
    par_idsufno_interne_pub = mapped_column(String(255), server_default=text('NULL::character varying'))


class TPropDem(db.Model):
    __tablename__ = 't_prop_dem'
    __table_args__ = {'schema': SCHEMA}
    __table_args__ = (
        PrimaryKeyConstraint('idt_prop_dem', name='t_prop_dem_pkey'),
        Index('idx_t_prop_dem_idprocpte', 'idprocpte')
    )

    idt_prop_dem = mapped_column(BigInteger)
    idprodroit = mapped_column(String(14), server_default=text('NULL::character varying'))
    idprocpte = mapped_column(String(22), server_default=text('NULL::character varying'))
    idcom = mapped_column(String(9), server_default=text('NULL::character varying'))
    dnulp = mapped_column(String(9), server_default=text('NULL::character varying'))
    dnuper = mapped_column(String(9), server_default=text('NULL::character varying'))
    dforme = mapped_column(String(9), server_default=text('NULL::character varying'))
    ddenom = mapped_column(String(60), server_default=text('NULL::character varying'))
    dlign3 = mapped_column(String(30), server_default=text('NULL::character varying'))
    dlign4 = mapped_column(String(36), server_default=text('NULL::character varying'))
    dlign5 = mapped_column(String(30), server_default=text('NULL::character varying'))
    dlign6 = mapped_column(String(32), server_default=text('NULL::character varying'))
    ccodro = mapped_column(String(9), server_default=text('NULL::character varying'))
    modif = mapped_column(Boolean)
    suppr = mapped_column(Boolean)
    ajout = mapped_column(Boolean)
    civilite = mapped_column(String(30), server_default=text('NULL::character varying'))
    clef = mapped_column(String(25), server_default=text('NULL::character varying'))


class TProprietaires(db.Model):
    __tablename__ = 't_proprietaires'
    __table_args__ = {'schema': SCHEMA}
    __table_args__ = (
        PrimaryKeyConstraint('idt_proprietaires', name='t_proprietaires_pkey'),
        Index('idx_t_proprietaires_idprocpte', 'idprocpte')
    )

    idt_proprietaires = mapped_column(BigInteger)
    idprodroit = mapped_column(String(14), server_default=text('NULL::character varying'))
    idprocpte = mapped_column(String(22), server_default=text('NULL::character varying'))
    idcom = mapped_column(String(9), server_default=text('NULL::character varying'))
    dnulp = mapped_column(String(9), server_default=text('NULL::character varying'))
    dnuper = mapped_column(String(9), server_default=text('NULL::character varying'))
    dforme = mapped_column(String(9), server_default=text('NULL::character varying'))
    ddenom = mapped_column(String(60), server_default=text('NULL::character varying'))
    dlign3 = mapped_column(String(30), server_default=text('NULL::character varying'))
    dlign4 = mapped_column(String(36), server_default=text('NULL::character varying'))
    dlign5 = mapped_column(String(30), server_default=text('NULL::character varying'))
    dlign6 = mapped_column(String(32), server_default=text('NULL::character varying'))
    ccodro = mapped_column(String(9), server_default=text('NULL::character varying'))
    modif = mapped_column(Boolean)
    suppr = mapped_column(Boolean)
    ajout = mapped_column(Boolean)
    civilite = mapped_column(String(30), server_default=text('NULL::character varying'))
    clef = mapped_column(String(25), server_default=text('NULL::character varying'))


class TTypeAtelier(db.Model):
    __tablename__ = 't_type_atelier'
    __table_args__ = {'schema': SCHEMA}
    __table_args__ = (
        PrimaryKeyConstraint('idt_type_atelier', name='t_type_atelier_pkey'),
    )

    id = mapped_column(BigInteger, nullable=False)
    idt_type_atelier = mapped_column(BigInteger)
    lib_atelier = mapped_column(String(100), server_default=text('NULL::character varying'))


class TUnite(db.Model):
    __tablename__ = 't_unite'
    __table_args__ = {'schema': SCHEMA}
    __table_args__ = (
        PrimaryKeyConstraint('id', name='t_unite_pkey'),
    )

    id = mapped_column(BigInteger)
    idt_unite = mapped_column(BigInteger)
    libunite = mapped_column(String(100), server_default=text('NULL::character varying'))


class TUsadresse(db.Model):
    __tablename__ = 't_usadresse'
    __table_args__ = {'schema': SCHEMA}
    __table_args__ = (
        PrimaryKeyConstraint('idt_usadresse', name='t_usadresse_pkey'),
    )

    idt_usadresse = mapped_column(BigInteger)
    adr_pacage = mapped_column(String(9), server_default=text('NULL::character varying'))
    adr_postale_1 = mapped_column(String(255), server_default=text('NULL::character varying'))
    adr_postale_2 = mapped_column(String(255), server_default=text('NULL::character varying'))
    adr_postale_3 = mapped_column(String(2555), server_default=text('NULL::character varying'))
    adr_postaleinsee = mapped_column(String(5), server_default=text('NULL::character varying'))
    adr_postaltel = mapped_column(String(10), server_default=text('NULL::character varying'))
    adr_mail = mapped_column(String(255), server_default=text('NULL::character varying'))
    adr_exploi_1 = mapped_column(String(255), server_default=text('NULL::character varying'))
    adr_exploi_2 = mapped_column(String(255), server_default=text('NULL::character varying'))
    adr_exploi_3 = mapped_column(String(255), server_default=text('NULL::character varying'))
    adr_exploinsee = mapped_column(BigInteger)
    adr_exploitel = mapped_column(String(255), server_default=text('NULL::character varying'))
    adr_portable1 = mapped_column(String(255), server_default=text('NULL::character varying'))
    adr_portable2 = mapped_column(String(255), server_default=text('NULL::character varying'))
    adr_postalcp = mapped_column(String(255), server_default=text('NULL::character varying'))
    adr_exploitcp = mapped_column(String(255), server_default=text('NULL::character varying'))


class TUsager(db.Model):
    __tablename__ = 't_usager'
    __table_args__ = {'schema': SCHEMA}
    __table_args__ = (
        PrimaryKeyConstraint('idt_usager', name='t_usager_pkey'),
    )

    idt_usager = mapped_column(BigInteger)
    u_pacage = mapped_column(String(9), server_default=text('NULL::character varying'))
    u_civilite = mapped_column(String(12), server_default=text('NULL::character varying'))
    u_nom_raison_sociale = mapped_column(String(40), server_default=text('NULL::character varying'))
    u_prenoms = mapped_column(String(30), server_default=text('NULL::character varying'))
    u_forme_juridique = mapped_column(String(50), server_default=text('NULL::character varying'))
    u_siret = mapped_column(String(14), server_default=text('NULL::character varying'))
    u_msa = mapped_column(String(14), server_default=text('NULL::character varying'))
    u_etat = mapped_column(String(10), server_default=text('NULL::character varying'))
    u_date_debut_validite_sigc = mapped_column(String(10), server_default=text('NULL::character varying'))
    u_date_fin_validite_sigc = mapped_column(String(10), server_default=text('NULL::character varying'))
    u_date_cloture = mapped_column(String(10), server_default=text('NULL::character varying'))
    u_civilite_edit = mapped_column(String(30), server_default=text('NULL::character varying'))

'''
class TParceldem(db.Model):
    __tablename__ = 't_parceldem'
    __table_args__ = {'schema': SCHEMA}
    __table_args__ = (
        ForeignKeyConstraint(['par_idsuf'], ['t_cadastre.idsuf'], name='fk_par_idsuf'),
        PrimaryKeyConstraint('idt_parceldem', name='t_parceldem_pkey'),
        Index('idx_t_parceldem_par_nointerne_par_idsuf', 'par_nointerne', 'par_idsuf')
    )

    idt_parceldem = mapped_column(BigInteger)
    par_nointerne = mapped_column(String(36), server_default=text('NULL::character varying'))
    par_insee = mapped_column(BigInteger)
    par_idsuf = mapped_column(String(17), server_default=text('NULL::character varying'))
    par_section = mapped_column(String(3), server_default=text('NULL::character varying'))
    par_parcelle = mapped_column(BigInteger)
    par_subdi = mapped_column(String(3), server_default=text('NULL::character varying'))
    par_surface = mapped_column(String(11), server_default=text('NULL::character varying'))
    par_idpropr = mapped_column(String(17), server_default=text('NULL::character varying'))
    par_insecpasu = mapped_column(String(23), server_default=text('NULL::character varying'))
    par_ok = mapped_column(Boolean, server_default=text('false'))
    par_bio = mapped_column(Boolean, server_default=text('false'))
    par_echange = mapped_column(Boolean, server_default=text('false'))
    par_deplanimaux = mapped_column(Boolean, server_default=text('false'))
    par_nointernepar_idproprpar_insee = mapped_column(String(30), server_default=text('NULL::character varying'))
    par_nointernepar_idpropr = mapped_column(String(24), server_default=text('NULL::character varying'))
    par_nointernepar_insee = mapped_column(Text)
    par_est_modif = mapped_column(Boolean, server_default=text('true'))
    par_nointernepar_idsuf = mapped_column(Text)
    par_dist_siege = mapped_column(String(11), server_default=text('NULL::character varying'))
    par_surf5 = mapped_column(String(11), server_default=text('NULL::character varying'))
    par_sur5a10 = mapped_column(String(11), server_default=text('NULL::character varying'))
    par_surf10 = mapped_column(String(11), server_default=text('NULL::character varying'))
    par_type_surf = mapped_column(Boolean, server_default=text('false'))
    par_vol = mapped_column(String(11), server_default=text('NULL::character varying'))
    par_cal = mapped_column(String(11), server_default=text('NULL::character varying'))
    par_export = mapped_column(Boolean, server_default=text('false'))
    par_prox = mapped_column(Boolean, server_default=text('false'))
    par_liaison = mapped_column(Boolean, server_default=text('false'))
    parc_enclave = mapped_column(Boolean, server_default=text('false'))
    par_export_sig = mapped_column(Boolean, server_default=text('false'))
    parc_zsce = mapped_column(Boolean, server_default=text('false'))
    par_volsiege = mapped_column(String(11), server_default=text('NULL::character varying'))

    t_cadastre: Mapped[Optional['TParceldem']] = relationship('TCadastre', back_populates='t_parceldem')
'''
class TParceldem(db.Model):
    __tablename__ = 't_parceldem'
    __table_args__ = (
        ForeignKeyConstraint(
            ['par_idsuf'],
            [f"{SCHEMA}.t_cadastre.idsuf"],
            name='fk_par_idsuf'
        ),
        PrimaryKeyConstraint('idt_parceldem', name='t_parceldem_pkey'),
        {"schema": SCHEMA}
    )

    idt_parceldem = mapped_column(BigInteger)
    par_nointerne = mapped_column(String(36), server_default=text('NULL::character varying'))
    par_insee = mapped_column(BigInteger)
    par_idsuf = mapped_column(String(17), nullable=False)
    par_section = mapped_column(String(3), server_default=text('NULL::character varying'))
    par_parcelle = mapped_column(BigInteger)
    par_subdi = mapped_column(String(3), server_default=text('NULL::character varying'))
    par_surface = mapped_column(String(11), server_default=text('NULL::character varying'))
    par_idpropr = mapped_column(String(17), server_default=text('NULL::character varying'))
    par_insecpasu = mapped_column(String(23), server_default=text('NULL::character varying'))
    par_ok = mapped_column(Boolean, server_default=text('false'))
    par_bio = mapped_column(Boolean, server_default=text('false'))
    par_echange = mapped_column(Boolean, server_default=text('false'))
    par_deplanimaux = mapped_column(Boolean, server_default=text('false'))
    par_nointernepar_idproprpar_insee = mapped_column(String(30), server_default=text('NULL::character varying'))
    par_nointernepar_idpropr = mapped_column(String(24), server_default=text('NULL::character varying'))
    par_nointernepar_insee = mapped_column(Text)
    par_est_modif = mapped_column(Boolean, server_default=text('true'))
    par_nointernepar_idsuf = mapped_column(Text)
    par_dist_siege = mapped_column(String(11), server_default=text('NULL::character varying'))
    par_surf5 = mapped_column(String(11), server_default=text('NULL::character varying'))
    par_sur5a10 = mapped_column(String(11), server_default=text('NULL::character varying'))
    par_surf10 = mapped_column(String(11), server_default=text('NULL::character varying'))
    par_type_surf = mapped_column(Boolean, server_default=text('false'))
    par_vol = mapped_column(String(11), server_default=text('NULL::character varying'))
    par_cal = mapped_column(String(11), server_default=text('NULL::character varying'))
    par_export = mapped_column(Boolean, server_default=text('false'))
    par_prox = mapped_column(Boolean, server_default=text('false'))
    par_liaison = mapped_column(Boolean, server_default=text('false'))
    parc_enclave = mapped_column(Boolean, server_default=text('false'))
    par_export_sig = mapped_column(Boolean, server_default=text('false'))
    parc_zsce = mapped_column(Boolean, server_default=text('false'))
    par_volsiege = mapped_column(String(11), server_default=text('NULL::character varying'))

    t_cadastre = relationship('TCadastre', back_populates='t_parceldem')


# --- Association Table for Many-to-Many (Users <-> UnitTasks) ---
agent_tasks = Table(
    "agent_tasks",
    db.metadata,
    Column("user_id", Integer, ForeignKey(f"{SCHEMA}.users.id", ondelete="CASCADE"), primary_key=True),
    Column("task_id", Integer, ForeignKey(f"{SCHEMA}.unit_tasks.id", ondelete="CASCADE"), primary_key=True),
    schema=SCHEMA
)

# --- Units ---
class Units(db.Model):
    __tablename__ = "units"
    __table_args__ = {'schema': SCHEMA}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)

    unit_tasks: Mapped[List["UnitTasks"]] = relationship(
        "UnitTasks", back_populates="unit", cascade="all, delete-orphan"
    )
    users: Mapped[List["Users"]] = relationship(
        "Users", back_populates="unit", cascade="all, delete-orphan"
    )

# --- UnitTasks ---
class UnitTasks(db.Model):
    __tablename__ = "unit_tasks"
    __table_args__ = {'schema': SCHEMA}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    unit_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(f"{SCHEMA}.units.id", ondelete="CASCADE"), nullable=False
    )
    description: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50), server_default=text("'À faire'::character varying"))

    unit: Mapped["Units"] = relationship("Units", back_populates="unit_tasks")

    # Existing relationship
    users: Mapped[List["Users"]] = relationship(
        "Users", secondary=agent_tasks, back_populates="tasks"
    )

    # Add this for convenience
    agents: Mapped[List["Users"]] = relationship(
        "Users",
        secondary=agent_tasks,
        back_populates="tasks",
        lazy="dynamic"
    )


# --- Users ---
class Users(UserMixin, db.Model):
    __tablename__ = "users"
    __table_args__ = {'schema': SCHEMA}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(512), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    unit_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey(f"{SCHEMA}.units.id", ondelete="SET NULL")
    )

    unit: Mapped[Optional["Units"]] = relationship("Units", back_populates="users")
    tasks: Mapped[List["UnitTasks"]] = relationship(
        "UnitTasks", secondary=agent_tasks, back_populates="users"
    )
    categories: Mapped[List["Category"]] = relationship(
        "Category", back_populates="user", cascade="all, delete-orphan"
    )
    transactions: Mapped[List["Transaction"]] = relationship(
        "Transaction", back_populates="user", cascade="all, delete-orphan"
    )

# --- Category ---
class Category(db.Model):
    __tablename__ = "categories"
    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_user_category"),
        {"schema": SCHEMA},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(f"{SCHEMA}.users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    user: Mapped["Users"] = relationship("Users", back_populates="categories")
    transactions: Mapped[List["Transaction"]] = relationship(
        "Transaction", back_populates="category", cascade="all, delete-orphan"
    )

# --- Transaction ---
class Transaction(db.Model):
    __tablename__ = "transactions"
    __table_args__ = {"schema": SCHEMA}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(f"{SCHEMA}.users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    category_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey(f"{SCHEMA}.categories.id", ondelete="SET NULL"), index=True
    )
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    type: Mapped[str] = mapped_column(String(10), nullable=False)  # 'income' or 'expense'
    description: Mapped[Optional[str]] = mapped_column(Text)
    date: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)

    user: Mapped["Users"] = relationship("Users", back_populates="transactions")
    category: Mapped[Optional["Category"]] = relationship("Category", back_populates="transactions")

class Groups(db.Model):
    __tablename__ = "groups"
    __table_args__ = {"schema": SCHEMA}
    __table_args__ = (
        PrimaryKeyConstraint('id', name='groups_pkey'),
        UniqueConstraint('name', name='groups_name_key')
    )

    id = mapped_column(Integer)
    name = mapped_column(String(20), nullable=False)
    created_at = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    items_groups: Mapped[List['ItemsGroups']] = relationship('ItemsGroups', uselist=True, back_populates='group')



class LeftItems(db.Model):
    __tablename__ = "left_items"
    __table_args__ = {"schema": SCHEMA}
    __table_args__ = (
        PrimaryKeyConstraint('id', name='left_items_pkey'),
    )

    id = mapped_column(Integer)
    name = mapped_column(String(50), nullable=False)

class RightItems(db.Model):
    __tablename__ = "right_items"
    __table_args__ = {"schema": SCHEMA}
    __table_args__ = (
        PrimaryKeyConstraint('id', name='right_items_pkey'),
    )

    id = mapped_column(Integer)
    name = mapped_column(String(50), nullable=False)

class ItemsGroups(db.Model):
    __tablename__ = "items_groups"
    __table_args__ = {"schema": SCHEMA}
    __table_args__ = (
        CheckConstraint("side::text = ANY (ARRAY['left'::character varying, 'right'::character varying]::text[])", name='items_groups_side_check'),
        ForeignKeyConstraint(['group_id'], ['groups.id'], ondelete='CASCADE', name='items_groups_group_id_fkey'),
        PrimaryKeyConstraint('id', name='items_groups_pkey'),
        UniqueConstraint('group_id', 'item_id', 'side', name='items_groups_group_id_item_id_side_key')
    )

    id = mapped_column(Integer)
    item_id = mapped_column(Integer, nullable=False)
    item_name = mapped_column(String(255), nullable=False)
    group_id = mapped_column(Integer)
    side = mapped_column(String(10))

    group: Mapped[Optional['Groups']] = relationship('Groups', back_populates='items_groups')



class TreeCategories(db.Model):
    __tablename__ = "tree_categories"
    __table_args__ = (
        ForeignKeyConstraint(
            ["parent_id"],
            [f"{SCHEMA}.tree_categories.id"],   # 🔧 préciser le schéma
            ondelete="CASCADE",
            name="tree_categories_parent_id_fkey"
        ),
        PrimaryKeyConstraint("id", name="tree_categories_pkey"),
        {"schema": SCHEMA}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    parent_id = Column(Integer, db.ForeignKey(f"{SCHEMA}.tree_categories.id"))

    # relation enfants/parent
    children: Mapped[list["TreeCategories"]] = relationship(
        "TreeCategories",
        backref=db.backref("parent", remote_side=[id]),
        cascade="all, delete-orphan"
    )

    # relation avec UserSelections
    user_selections: Mapped[list["UserSelections"]] = relationship(
        "UserSelections",
        back_populates="category",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "parent_id": self.parent_id,
            "children": [child.to_dict() for child in self.children]
        }


class UserSelections(db.Model):
    __tablename__ = "user_selections"
    __table_args__ = (
        ForeignKeyConstraint(
            ["category_id"],
            [f"{SCHEMA}.tree_categories.id"],   # 🔧 préciser le schéma
            ondelete="CASCADE",
            name="user_selections_category_id_fkey"
        ),
        PrimaryKeyConstraint("id", name="user_selections_pkey"),
        UniqueConstraint("user_id", "category_id", name="user_selections_user_id_category_id_key"),
        {"schema": SCHEMA}
    )

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, nullable=False)
    category_id = mapped_column(Integer, nullable=False)

    category: Mapped["TreeCategories"] = relationship(
        "TreeCategories",
        back_populates="user_selections"
    )
