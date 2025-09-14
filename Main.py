from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from controllers import login
from controllers.login import auth_bp

app = Flask(__name__)

app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
csrf = CSRFProtect(app)

app.register_blueprint(auth_bp, url_prefix='/bugig') 

# fazer um teste se tirar o .login funciona para importar tudo
from controllers.login import *
from controllers.public_routes import *


if __name__ == '__main__':
    app.run(debug=True, port=5001)

    # teste
