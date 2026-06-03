from flask import current_app, redirect, url_for, session
from functools import wraps
import uuid
import datetime

tokens = {}

def generate_token():
  token = str(uuid.uuid4())
  tokens[token] = datetime.datetime.now()
  return token

def is_valid_token(token: str):
  return token in tokens and (datetime.datetime.now() - tokens[token]).total_seconds() < current_app.config['LIFETIME']

def remove_token(token: str):
  if token in tokens:
    del tokens[token]

def login_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    token = session.get('token')
    if not token or not is_valid_token(token):
      return redirect(url_for('files.login'))
    return f(*args, **kwargs)
  return decorated