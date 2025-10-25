from flask import Blueprint, render_template, redirect, url_for

# Definindo o blueprint
public_bp = Blueprint('public', __name__)

# Rota raiz redireciona para a landing page
@public_bp.route('/')
def index():
    return redirect(url_for('public.landing_page'))

# Rota da landing page
@public_bp.route('/landingPage')
def landing_page():
    return render_template('LandingPage.html')

# Rota da página sobre
@public_bp.route('/about')
def about():
    return render_template('about.html')
