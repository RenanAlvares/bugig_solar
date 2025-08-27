from Main import app
from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from forms.FormUser import FormUser
from forms.FormUser import FormLogin


# rota de cadastro 

@app.route('/signin', methods=['POST', 'GET'])
def cadastro():
    form = FormUser()
    titulo = 'Cadastro'
    if form.validate_on_submit():
        nome = form.nome.data
        tipo_usuario = int(form.tipo_usuario.data)  # transforma string para int para salvar no banco como fk
        return redirect(url_for('cadastro'))
    return render_template('Cadastro.html', titulo=titulo, form=form)


@app.route('/authenticate')
def authenticate():
    pass

@app.route('/')
def login():
    return render_template('Login.html', titulo='teste')

# rota de login 
@app.route('/', methods=['POST', 'GET'])
def login():
    form = FormLogin()
    titulo = 'Login'
    if form.validate_on_submit():
        email = form.email.data
        senha = form.senha.data
        return redirect(url_for('login'))
    return render_template('login.html', titulo=titulo, form=form)
