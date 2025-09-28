from flask import Flask
from extensions import db, csrf

from controllers.public_routes import public_bp
from controllers.login import auth_bp  # importa blueprint já com todas as rotas

app = Flask(__name__)
app.config.from_pyfile('config.py')

db.init_app(app)
csrf.init_app(app)

# registra blueprints
app.register_blueprint(public_bp)
app.register_blueprint(auth_bp, url_prefix='/bugig')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
