from cryptography.fernet import Fernet

_fernet = None

def get_or_create_key(key_path):
  try:
    with open(key_path, 'rb') as key_file:
      key = key_file.read()
  except FileNotFoundError:
    key = Fernet.generate_key()
    with open(key_path, 'wb') as key_file:
      key_file.write(key)
  return key

def init_crypto(key_path):
    global _fernet
    key = get_or_create_key(key_path)
    _fernet = Fernet(key)

def encrypt_file(data: bytes) -> bytes:
  return _fernet.encrypt(data)

def decrypt_file(data: bytes) -> bytes:
  return _fernet.decrypt(data)