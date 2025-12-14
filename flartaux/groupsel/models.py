from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#db = SQLAlchemy()
from ..database import db
from sqlalchemy import Table, Column, Integer, Text, Date, Boolean, String, ForeignKey
from sqlalchemy import create_engine, Column, Integer, BigInteger, Text, Date, Boolean, String, MetaData, Table
from sqlalchemy import PrimaryKeyConstraint, Index, UniqueConstraint, ForeignKeyConstraint
# models.py
"""
class TCadastre(db.Model):
    __tablename__ = 't_cadastre'

    __table_args__ = (
        PrimaryKeyConstraint('idt_cadastre', name='t_cadastre_pkey'),
    )

    idt_cadastre = db.Column(db.BigInteger, primary_key=True)
    idsuf = db.Column(db.String(16), unique=True, nullable=False)
    idpar = db.Column(db.String(16), unique=True, nullable=False)
    idprocpte = db.Column(db.String(16), unique=True, nullable=False)
    idcom = db.Column(db.String(5), unique=True, nullable=False)
    ccosec = db.Column(db.String(2), unique=True, nullable=False)
    dnupla = db.Column(db.String(4), unique=True, nullable=False)
    ccosub = db.Column(db.String(2), unique=True, nullable=False)
    dcntsf = db.Column(BigInteger)
    idprocpte_org = db.Column(Text)
"""
class TProprietaires(db.Model):
    __tablename__ = 't_proprietaires'
    __table_args__ = (
        PrimaryKeyConstraint('idt_proprietaires', name='t_proprietaires_pkey'),
        Index('idx_t_proprietaires_idprocpte', 'idprocpte')
    )
    """
    __table_args__ = (
        PrimaryKeyConstraint('idt_proprietaires', name='t_proprietaires_pkey'),
    )
    """
    idt_proprietaires = db.Column(db.BigInteger, primary_key=True)
    idprodroit = db.Column(db.String(13), unique=True, nullable=False)
    idprocpte = db.Column(db.String(22), unique=True, nullable=False)
    idcom = db.Column(db.String(9), unique=True, nullable=False)
    dnulp = db.Column(db.String(9), unique=True, nullable=False)
    dnuper = db.Column(db.String(9), unique=True, nullable=False)
    dforme = db.Column(db.String(9), unique=True, nullable=False)
    ddenom = db.Column(db.String(60), unique=True, nullable=False)
    dlign3 = db.Column(db.String(30), unique=True, nullable=False)
    dlign4 = db.Column(db.String(36), unique=True, nullable=False)
    dlign5 = db.Column(db.String(30), unique=True, nullable=False)
    dlign6 = db.Column(db.String(32), unique=True, nullable=False)
    ccodro = db.Column(db.String(9), unique=True, nullable=False)
    modif = db.Column(db.Boolean)
    suppr = db.Column(db.Boolean)
    ajout = db.Column(db.Boolean)
    civilite = db.Column(db.String(30), unique=True, nullable=False)
    clef = db.Column(db.String(25), unique=True, nullable=False)

class TProp_dem(db.Model):
    __tablename__ = 't_prop_dem'
    __table_args__ = (
        PrimaryKeyConstraint('idt_prop_dem', name='t_prop_dem_pkey'),
        Index('idx_t_prop_dem_idprocpte', 'idprocpte')
    )
    """
    __table_args__ = (
        PrimaryKeyConstraint('idt_proprietaires', name='t_proprietaires_pkey'),
    )
    """
    idt_prop_dem = db.Column(db.BigInteger, primary_key=True)
    idprodroit = db.Column(db.String(13), unique=True, nullable=False)
    idprocpte = db.Column(db.String(22), unique=True, nullable=False)
    idcom = db.Column(db.String(9), unique=True, nullable=False)
    dnulp = db.Column(db.String(9), unique=True, nullable=False)
    dnuper = db.Column(db.String(9), unique=True, nullable=False)
    dforme = db.Column(db.String(9), unique=True, nullable=False)
    ddenom = db.Column(db.String(60), unique=True, nullable=False)
    dlign3 = db.Column(db.String(30), unique=True, nullable=False)
    dlign4 = db.Column(db.String(36), unique=True, nullable=False)
    dlign5 = db.Column(db.String(30), unique=True, nullable=False)
    dlign6 = db.Column(db.String(32), unique=True, nullable=False)
    ccodro = db.Column(db.String(9), unique=True, nullable=False)
    modif = db.Column(db.Boolean)
    suppr = db.Column(db.Boolean)
    ajout = db.Column(db.Boolean)
    civilite = db.Column(db.String(30), unique=True, nullable=False)
    clef = db.Column(db.String(25), unique=True, nullable=False)

class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Add this field
    items = db.relationship('ItemGroup', backref='group', cascade='all, delete-orphan')


class LeftItem(db.Model):
    __tablename__ = 'left_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class RightItem(db.Model):
    __tablename__ = 'right_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class ItemGroup(db.Model):
    __tablename__ = 'items_groups'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id', ondelete='CASCADE'), nullable=False)
    item_name = db.Column(db.String(50), nullable=False)
    column_type = db.Column(db.String(10), nullable=False)  # 'left' or 'right'
    selection_order = db.Column(db.Integer, nullable=False)  # Add an order field to store the order of selection

