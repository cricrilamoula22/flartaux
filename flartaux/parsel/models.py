from ..database import db
from sqlalchemy import Table, Column, Integer, Text, Date, Boolean, String, ForeignKey
from sqlalchemy import create_engine, Column, Integer, BigInteger, Text, Date, Boolean, String, MetaData, Table

class TParceldem(db.Model):    
    __tablename__ = 't_parceldem'
    idt_parceldem = Column(BigInteger, primary_key=True)
    par_nointerne = Column(String(9))
    par_insee = Column(BigInteger)
    par_idsuf = Column(String(16))
    par_section = Column(String(2))
    par_parcelle = Column(BigInteger)
    par_subdi = Column(String(2))
    par_surface = Column(String(10))
    par_idpropr = Column(String(11))
    par_insecpasu = Column(String(22))
    par_ok = Column(Boolean)
    par_bio = Column(Boolean)
    par_echange = Column(Boolean)
    par_deplanimaux = Column(Boolean)
    par_nointernepar_idproprpar_insee = Column(String(29))
    par_nointernepar_idpropr = Column(String(23))
    par_nointernepar_insee = Column(Text)
    par_est_modif = Column(Boolean)
    par_nointernepar_idsuf = Column(Text)
    par_dist_siege = Column(String(10))
    par_surf5 = Column(String(10))
    par_sur5a10 = Column(String(10))
    par_surf10 = Column(String(10))
    par_type_surf = Column(Boolean)
    par_vol = Column(String(10))
    par_cal = Column(String(10))
    par_export = Column(Boolean)
    par_prox = Column(Boolean)
    par_liaison = Column(Boolean)
    parc_enclave = Column(Boolean)
    par_export_sig = Column(Boolean)
    parc_zsce = Column(Boolean)
    par_volsiege = Column(String(10))

class TCom2023(db.Model):
    __tablename__ = 't_com2023'

    idt_com2023 = Column(BigInteger, primary_key=True, autoincrement=True)
    com = Column(String(5))
    dep = Column(String(3))
    can = Column(String(5))
    libelle = Column(String(255))
    
class TCadastre(db.Model):
    __tablename__ = 't_cadastre'

    idt_cadastre = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    idsuf = db.Column(db.String(16))
    idpar = db.Column(db.String(16))
    idprocpte = db.Column(db.String(16))
    idcom = db.Column(db.String(5))
    ccosec = db.Column(db.String(2))
    dnupla = db.Column(db.String(4))
    ccosub = db.Column(db.String(2))
    dcntsf = db.Column(db.BigInteger)
    idprocpte_org = db.Column(db.Text)