# Flashdrop 

Flashdrop is a lightweight Flask web application designed for secure file transfer and storage within a local area network (LAN). Uploaded files are automatically encrypted server-side and stored securely.

## Features

- **Authentication**: Global password protection to secure your local hub access.
- **Server-Side Encryption**: Files are encrypted using the `cryptography` library (Fernet) as soon as they are received and decrypted on the fly upon download.
- **Local HTTPS**: Native SSL configuration ensuring that file transfers across your local Wi-Fi network remain confidential.
- **Simple UI**: Clean drag-and-drop area with a real-time upload progress bar.

---

## Prerequisites

Before setting up Flashdrop, ensure you have the following installed on your system:
- **Python 3.8+**
- **OpenSSL** (Pre-installed on most Linux/macOS systems; required to generate local SSL certificates)

---

## Installation & Configuration

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/flashdrop.git](https://github.com/your-username/flashdrop.git)
cd flashdrop
```

### 2. Create a Virtual Environment and Install Dependencies

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the environment (Linux/macOS)
source venv/bin/activate

# Activate the environment (Windows)
# venv\Scripts\activate

# Install required Python packages
pip install -r requirements.txt
```
(Note: If you haven't created a requirements.txt file yet, create one and add: Flask, cryptography, and python-dotenv)

### 3. Environment Variables Configuration (.env)

For security reasons, secret keys and passwords are not included in the repository. You must create your own local .env file at the root of the project.

##### 1 - Create a file named .env:
```bash
touch .env
```
##### 2 - Open it and define your own custom credentials and keys:
Code snippet

```
SECRET_KEY=put_a_very_long_random_secret_key_here
PASSWORD=your_secure_password_to_log_in
```

### 4. Generate SSL Certificates (Required for HTTPS)

The application relies on HTTPS to securely run locally on port 5443. To allow the server to start, you must generate an SSL certificate pair (certificate and private key) inside a certs/ directory at the project root.

Run the following commands in your terminal:

```bash
# Create the required directories if they don't exist
mkdir -p certs uploads

# Generate a self-signed certificate valid for 365 days
openssl req -x509 -newkey rsa:4096 -nodes -keyout certs/key.pem -out certs/cert.pem -days 365 -subj "/CN=localhost"
```

## Running the Application

Once the configuration is complete, start the Flask development server:

```bash
python run.py
```

The application will be accessible from your local machine at:

-> https://localhost:5443/login
Accessing Flashdrop from a Smartphone (iPhone/Android) on the same network

Find your computer's local IP address.

Open your mobile browser and enter the exact address (manually appending /login at the end):

-> https://X.X.X.X:5443/login

Note on Local HTTPS: Since the SSL certificate is self-signed, your browser will display a security warning ("Your connection is not private"). Click on "Advanced" or "Show details", then choose "Proceed to website" to bypass it.

## Project Structure

```plaintext
├── app/
│   ├── __init__.py    # Initializes the Flask app and encryption setup
│   ├── auth.py        # Token-based session management & login middleware
│   ├── config.py      # Environment variables loader
│   ├── crypto.py      # Fernet encryption/decryption functions
│   ├── routes.py      # App routes (upload, download, auth management)
│   └── templates/
│       ├── index.html # Main file manager interface
│       └── login.html # Authentication page
├── certs/             # Local SSL certificates & auto-generated secret.key (IGNORED BY GIT)
├── uploads/           # Destination folder for encrypted files (.enc) (IGNORED BY GIT)
├── .env               # Local configuration file (IGNORED BY GIT)
├── .gitignore         # Prevents sensitive files from being pushed
└── run.py             # Application entry point
```

## Security & Production Notes

This project is tailored for personal and local network usage. On the very first run, a secret.key file is automatically generated inside the certs/ directory if it does not exist yet.

Do not lose or delete this secret.key file. If you delete it, it will be mathematically impossible to decrypt any files previously uploaded to your uploads/ folder.