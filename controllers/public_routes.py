from flask import Blueprint, render_template, redirect, url_for
from sqlalchemy import func
from models_DB.users import UsersDb
from models_DB.donation_queue import Donation, Queue

# Definindo o blueprint
public_bp = Blueprint('public', __name__)

# Rota raiz redireciona para a landing page
@public_bp.route('/')
def index():
    return redirect(url_for('public.landing_page'))

# Rota da landing page
@public_bp.route('/landingPage')
def landing_page():
    
    usuarios = UsersDb.query.count()

    qtd_creditos = (
        Donation.query
        .with_entities(func.sum(Donation.quantidade_doacao))
        .filter(Donation.status == False)
        .scalar() or 0
    )

    qtd_recebidos = (
        Queue.query
        .with_entities(func.sum(Queue.quantidade_recebida))
        .scalar() or 0
    )


    return render_template(
        'landing_page.html', 
        qtd_users=usuarios, 
        qtd_creditos=qtd_creditos,
        qtd_recebidos=qtd_recebidos
    )

# Rota da página sobre
@public_bp.route('/about')
def about():
    return render_template('about.html')
