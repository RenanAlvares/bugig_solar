from flask import render_template
from Main import app

@app.errorhandler(400)
def bad_request(error):
    return render_template('error.html', code=400, message="Requisição inválida"), 400

@app.errorhandler(401)
def unauthorized(error):
    return render_template('error.html', code=401, message="Não autorizado"), 401

@app.errorhandler(403)
def forbidden(error):
    return render_template('error.html', code=403, message="Acesso negado"), 403

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', code=404, message="Página não encontrada"), 404

@app.errorhandler(405)
def method_not_allowed(error): 
    return render_template('error.html', code=405, message="Método não permitido"), 405

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error.html', code=500, message="Erro interno do servidor"), 500


