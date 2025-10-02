from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

# IMPORTANTE: importa todas as rotas **depois** de criar o blueprint
from . import login
from . import edit_cad
from . import cad_benef_gen
from . import get_in_queue