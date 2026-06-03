import os
from dotenv import load_dotenv

load_dotenv()

class Config:
  SECRET_KEY = os.getenv('SECRET_KEY')
  BASE_DIR = os.path.dirname(os.path.dirname(__file__))
  UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
  CERTS_FOLDER = os.path.join(BASE_DIR, 'certs')
  LIFETIME = 3600
  PASSWORD = os.getenv('PASSWORD')