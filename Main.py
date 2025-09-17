from flask import Flask, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from extensions import db, csrf

# importando os blueprints
from controllers.public_routes import public_bp
from controllers.login import auth_bp, login_required

app = Flask(__name__)
app.config.from_pyfile('config.py')

# registrando os blueprints
app.register_blueprint(public_bp)
app.register_blueprint(auth_bp, url_prefix='/bugig')

if __name__ == '__main__':
    app.run(debug=True, port=5001)


#aqui será a tela principal do sistema, onde o cliente é redirecionado após logar.
