from ..database import db
from sqlalchemy import Table, Column, Integer, Text, Date, Boolean, String, ForeignKey
from sqlalchemy import create_engine, Column, Integer, BigInteger, Text, Date, Boolean, String, MetaData, Table


class MainTable(db.Model):
    __tablename__ = 'main_table'    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

class SubTable(db.Model):
    __tablename__ = 'sub_table'    
    id = db.Column(db.Integer, primary_key=True)
    main_id = db.Column(db.Integer, db.ForeignKey('main_table.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    value = db.Column(db.String(255), nullable=False)

