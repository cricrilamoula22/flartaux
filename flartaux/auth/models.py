from ..database import db
from sqlalchemy import Table, Column, Integer, Text, Date, Boolean, String, ForeignKey
from sqlalchemy import create_engine, Column, Integer, BigInteger, Text, Date, Boolean, String, MetaData, Table
from flask_login import UserMixin 
from sqlalchemy.orm import relationship

class TUser(UserMixin, db.Model):
    __tablename__ = 't_user'
    id = db.Column(Integer, primary_key=True)
    username = db.Column(String(64), index=True, unique=True)
    email = db.Column(String(120), index=True, unique=True)
    password_hash = db.Column(String(256))
    password = db.Column(db.String(200), nullable=False)  # Ensure 'password' exists
"""
    roles = relationship(
        'Role',
        secondary='t_user_roles',
        primaryjoin='TUser.id == TUserRoles.user_id',
        secondaryjoin='Role.id == TUserRoles.role_id',
        back_populates='users'
    )
"""
class TRole(db.Model):
    __tablename__ = 't_role'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(64), index=True, unique=True)

# Model for the UserRoles table
class TUserRoles(db.Model):
    __tablename__ = 't_user_roles'
    id = db.Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('t_user.id'), primary_key=True)
    role_id = Column(Integer, ForeignKey('t_role.id'), primary_key=True)

# Now define relationships
TRole.users = relationship(
    'TUser', 
    secondary='t_user_roles', 
    back_populates='roles'
)

TUser.roles = relationship(
    'TRole', 
    secondary='t_user_roles', 
    back_populates='users'
)
    
