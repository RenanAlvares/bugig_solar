from flask import Blueprint, render_template, redirect, url_for, session
from Main import app

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def index():
    return redirect(url_for('landingPage'))

@public_bp.route('/landingPage')
def landingPage():
    return render_template('LandingPage.html')

@public_bp.route('/about')
def about():
    return render_template('about.html')