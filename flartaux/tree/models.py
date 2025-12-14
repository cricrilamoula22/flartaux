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

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)

    parent = db.relationship('Category', remote_side=[id], backref='children')

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.name,
            'children': [child.to_dict() for child in self.children]
        }

class UserSelection(db.Model):
    __tablename__ = 'user_selections'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'category_id', name='_user_category_uc'),
    )