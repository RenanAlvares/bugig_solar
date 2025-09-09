from functools import wraps
from Main import app, db
from flask import render_template, request, redirect, session, flash, url_for
from forms.FormUser import FormUser
from forms.FormLogin import FormLogin
from models_DB.Companies import Companies
from models_DB.Users import UsersDb

# decorador que verifica se o usuario está logado em outras sessoes
# ao chamar uma função que deve ser protegida, basta usar esse decorador e passar o id_usuario nos parametros da rota
# será utilizado se informarmos o id do usuário na url, ex: /user/1 
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Você precisa fazer login para acessar esta página.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function  


# rota de cadastro 
@app.route('/signin', methods=['POST', 'GET'])
def cadastro():
    form = FormUser()
    titulo = 'Cadastro'

    distribuidoras = Companies.query.all()
    
    #mostra todas as distribuidoras para selecionar no cadastro
    # form.distribuidora.choices = [(str(d.id_distribuidora), d.nome) for d in distribuidoras]
    
    if form.validate_on_submit():
        
        nome = form.nome.data
        tipo_usuario = int(form.tipo_usuario.data)  # transforma string para int para salvar no banco como fk
        email = form.email.data
        senha = form.senha.data

        if form.tipo_documento.data == 'cpf':
            documento = form.cpf.data
            razao_social = None
        else:
            documento = form.cnpj.data
            razao_social = form.nome_fantasia.data
        
        cep = form.cep.data
        numero = form.numero.data
        telefone = form.telefone.data
        id_distribuidora = int(form.distribuidora.data)

        if UsersDb.query.filter_by(email=email).first():
            flash('O e-mail informado já está em uso. Por favor, utilize outro e-mail.', 'danger')
            return redirect(url_for('cadastro'))

        novo_usuario = UsersDb(
            nome=nome,
            id_tipo=tipo_usuario,
            email=email,
            documento=documento,
            cep=cep,
            numero=numero,
            senha=senha,
            telefone=telefone,
            razao_social=razao_social,
            id_distribuidora=id_distribuidora
        )

        db.session.add(novo_usuario)
        db.session.commit()
        flash('Usuário cadastrado com sucesso!', 'success')

        return redirect(url_for('bugig'))
    
    return render_template('Cadastro.html', titulo=titulo, form=form)


# o sistema carrega e já altera a url para /bugig que será sempre a principal
@app.route('/')
def index():
    return redirect(url_for('landingPage'))

@app.route('/landingPage')
def landingPage():
    return render_template('landingPage.html')

#aqui será a tela principal do sistema, onde o cliente é redirecionado após logar.
@app.route('/bugig')
@login_required
def bugig():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    return render_template('bugig.html')


# rota de login 
@app.route('/login', methods=['POST', 'GET'])
def login():

    form = FormLogin()
    titulo = 'Login'

    if form.validate_on_submit():

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
