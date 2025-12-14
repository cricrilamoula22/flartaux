import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-prod")
    #SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///fintrack.db")
    #SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres:alt@127.0.0.1:5433/fintrack_project")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres:alt@127.0.0.1:5433/adl?options=-csearch_path%3Dw_sadr_artaux")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
