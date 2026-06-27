import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'rahasia_negara_123')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///recipe_platform.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False