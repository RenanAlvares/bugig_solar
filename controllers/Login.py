from Main import app
from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
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

# o sisteam carrega e já altera a url para /bugig
@app.route('/')
def index():
    return redirect(url_for('bugig'))


#aqui será a tela principal do sistema, onde o cliente é redirecionado após logar.
@app.route('/bugig')
def bugig():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    return render_template('bugig.html')


# autenticação do usuario no processo do sistema
@app.route('/authenticate')
def authenticate():
    pass

# rota de login 
@app.route('/login', methods=['POST', 'GET'])
def login():

    form = FormLogin()
    titulo = 'Login'

    if form.validate_on_submit():

        email = form.email.data
        senha = form.senha.data
        #usuario = UsersDb.query.filter_by(email=email).first()

        usuario_teste = {
            'id': 1,
            "email": "teste@teste.com",
            "senha": "123456"
        }

        if email == usuario_teste["email"] and senha == usuario_teste["senha"]:

            session['user_id'] = usuario_teste["id"]
            session['user_nome'] = usuario_teste["nome"]
            session['user_tipo'] = usuario_teste["id_tipo"]
            '''if usuario and usuario.senha == senha:
                session['user_id'] = usuario.id
                session['user_id'] = usuario.nome'''

            flash(f'Login efetuado com sucesso. Seja bem vindo!', 'success')
            return redirect(url_for('bugig'))
        else:

            flash('Email ou senha inválidos. Por favor, tente novamente!', 'danger')
            return redirect(url_for('bugig'))
        
    return render_template('login.html', titulo=titulo, form=form)
