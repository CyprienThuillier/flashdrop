from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', ssl_context=(app.config['CERTS_FOLDER'] + '/cert.pem', app.config['CERTS_FOLDER'] + '/key.pem'), port=5443)