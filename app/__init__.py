from flask import Flask
from app.config import Config
from app.crypto import init_crypto
from app.routes import files_bp
import os

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)
  app.register_blueprint(files_bp)
  with app.app_context():
    key_path = os.path.join(app.config['CERTS_FOLDER'], 'secret.key')
    init_crypto(key_path)
  return app