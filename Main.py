from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from controllers import Login

app = Flask(__name__)

app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

csrf = CSRFProtect(app)

from controllers.Views_client import *
#from views_users import *


if __name__ == '__main__':
    app.run(debug=True, port=5001)

    # teste
