from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#db = SQLAlchemy()
from ..database import db
from sqlalchemy import Table, Column, Integer, Text, Date, Boolean, String, ForeignKey
from sqlalchemy import create_engine, Column, Integer, BigInteger, Text, Date, Boolean, String, MetaData, Table
from sqlalchemy import PrimaryKeyConstraint, Index, UniqueConstraint, ForeignKeyConstraint

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from typing import List, Optional

class Products(db.Model):
    __tablename__ = 'products'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='products_pkey'),
    )

    id = db.Column(db.Integer)
    name = db.Column(db.Text)

    sales: Mapped[List['Sales']] = relationship('Sales', uselist=True, back_populates='product')


class Regions(db.Model):
    __tablename__ = 'regions'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='regions_pkey'),
    )

    id = db.Column(db.Integer)
    name = db.Column(db.Text)

    sales: Mapped[List['Sales']] = relationship('Sales', uselist=True, back_populates='region')


class Sales(db.Model):
    __tablename__ = 'sales'
    __table_args__ = (
        ForeignKeyConstraint(['product_id'], ['products.id'], name='sales_product_id_fkey'),
        ForeignKeyConstraint(['region_id'], ['regions.id'], name='sales_region_id_fkey'),
        PrimaryKeyConstraint('id', name='sales_pkey')
    )

    id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    region_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    price_per_unit = db.Column(db.Numeric)
    sales_date = db.Column(db.Date)

    product: Mapped[Optional['Products']] = relationship('Products', back_populates='sales')
    region: Mapped[Optional['Regions']] = relationship('Regions', back_populates='sales')

"""
class Sales(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String)
    product = db.Column(db.String)
    amount = db.Column(db.Integer)
"""  
"""
class Sales(db.Model):
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))
    product = db.relationship('Product', back_populates='sales')
    region = db.relationship('Region', back_populates='sales')

class Product(db.Model):
    sales = db.relationship('Sales', back_populates='product')

class Region(db.Model):
    sales = db.relationship('Sales', back_populates='region')

query = (
    db.session.query(Product.name, Region.name, Sales.amount)
    .join(Sales)
    .join(Region)
)
"""  
