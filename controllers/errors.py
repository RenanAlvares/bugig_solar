# controllers/errors.py
from flask import Blueprint, render_template

errors_bp = Blueprint('errors', __name__)

@errors_bp.app_errorhandler(400)
def bad_request(error):
    return render_template('errors.html', code=400, message="Requisição inválida"), 400

@errors_bp.app_errorhandler(401)
def unauthorized(error):
    return render_template('errors.html', code=401, message="Não autorizado"), 401

@errors_bp.app_errorhandler(403)
def forbidden(error):
    return render_template('errors.html', code=403, message="Acesso negado"), 403

@errors_bp.app_errorhandler(404)
def not_found(error):
    return render_template('errors.html', code=404, message="Página não encontrada"), 404

@errors_bp.app_errorhandler(405)
def method_not_allowed(error):
    return render_template('errors.html', code=405, message="Método não permitido"), 405

@errors_bp.app_errorhandler(500)
def internal_server_error(error):
    return render_template('errors.html', code=500, message="Erro interno do servidor"), 500
