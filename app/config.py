import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    OUTPUT_DIR = os.path.join(BASE_DIR, "static", "generated_docs")
