import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key-for-math-platform'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{BASE_DIR}/math_platform.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
