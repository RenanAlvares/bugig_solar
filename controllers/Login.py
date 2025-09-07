from functools import wraps
from Main import app
from flask import render_template, request, redirect, session, flash, url_for
from forms.FormUser import FormUser
from forms.FormLogin import FormLogin
from models_DB.Users import UsersDb


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


# o sistema carrega e já altera a url para /bugig que será sempre a principal
@app.route('/')
def index():
    return redirect(url_for('bugig'))


#aqui será a tela principal do sistema, onde o cliente é redirecionado após logar.
@app.route('/bugig')
def bugig():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    return render_template('bugig.html')


# decorador que verifica se o usuario está logado em outras sessoes
# ao chamar uma função que deve ser protegida, basta usar esse decorador e passar o id_usuario nos parametros da rota
def user_owns_resource(param_id_name):
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Você precisa fazer login para acessar esta página.', 'warning')
                return redirect(url_for('login'))
            
            # Pega o ID da URL dinamicamente
            url_id = kwargs.get(param_id_name)
            if url_id != session['user_id']:
                flash('Acesso negado a essa página.', 'danger')
                return redirect(url_for('login'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator    


# rota de login 
@app.route('/login', methods=['POST', 'GET'])
def login():

    form = FormLogin()
    titulo = 'Login'

    if form.validate_on_submit():
        print('form funcionou')

        email = form.email.data
        senha = form.senha.data
        usuario = UsersDb.query.filter_by(email=email).first()

        if usuario and usuario.senha == senha:
            
            # cria a session do ususário que será utilizada para validações de rotas
            session['user_id'] = usuario.id
            session['user_nome'] = usuario.nome
            session['user_tipo'] = usuario.id_tipo

            flash(f'Login efetuado com sucesso. Seja bem vindo!', 'success')
            return redirect(url_for('bugig'))
        else:

            flash('Email ou senha inválidos. Por favor, tente novamente!', 'danger')
            return redirect(url_for('login'))
        
    return render_template('login.html', titulo=titulo, form=form)
