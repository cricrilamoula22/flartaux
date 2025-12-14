import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'postgresql://postgres:alt@127.0.0.1:5433/flartaux'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = "simple"  # You can change this for different caching strategies.
    #CACHE_DEFAULT_TIMEOUT = 300  # Cache timeout in seconds.
    #CACHE_TYPE = "filesystem"
    #CACHE_DIR = "cache-dir"
    CACHE_DEFAULT_TIMEOUT = 922337203685477580
    CACHE_THRESHOLD = 922337203685477580
