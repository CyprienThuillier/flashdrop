from flask import current_app, Blueprint, render_template, request, session, redirect, url_for, jsonify, send_file
from app.auth import login_required, generate_token, remove_token
from werkzeug.utils import secure_filename
from app.crypto import encrypt_file, decrypt_file
import os
import io

files_bp = Blueprint('files', __name__)

@files_bp.route('/')
@login_required
def index():
  return render_template('index.html')

@files_bp.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    password = request.form.get('password')
    if password != current_app.config['PASSWORD']:
      return render_template('login.html', error='Invalid password')
    token = generate_token()
    session['token'] = token
    return redirect(url_for('files.index'))
  return render_template('login.html')

@files_bp.route('/upload', methods=['POST'])
@login_required
def upload():
  file = request.files.get('file')
  if not file:
    return jsonify({'success': False, 'error': 'No file provided'}), 400
  filename = secure_filename(file.filename)
  data = file.read()
  encrypted = encrypt_file(data)
  with open(os.path.join(current_app.config['UPLOAD_FOLDER'], filename + '.enc'), 'wb') as f:
      f.write(encrypted)
  return jsonify({'success': True, 'filename': filename}), 200

@files_bp.route('/download/<filename>', methods=['GET'])
@login_required
def download(filename):
  path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename + '.enc')
  if not os.path.exists(path):
    return jsonify({'success': False, 'error': 'File not found'}), 404
  with open(path, 'rb') as f:
    encrypted = f.read()
  decrypted = decrypt_file(encrypted)
  return send_file(io.BytesIO(decrypted), as_attachment=True, download_name=filename)

@files_bp.route('/files', methods=['GET'])
@login_required
def list_files():
  files = []
  for filename in os.listdir(current_app.config['UPLOAD_FOLDER']):
    if filename.endswith('.enc'):
      files.append(filename[:-4])
  return jsonify({'success': True, 'files': files}), 200

@files_bp.route('/logout', methods=['GET'])
@login_required
def logout():
  remove_token(session.get('token'))
  session.pop('token', None)
  return redirect(url_for('files.login'))