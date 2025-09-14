from flask import render_template, redirect, url_for, session
from Main import app

@app.route('/')
def index():
    return redirect(url_for('landingPage'))

@app.route('/landingPage')
def landingPage():
    return render_template('LandingPage.html')

@app.route('/about')
def about():
    return render_template('about.html')