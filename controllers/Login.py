from functools import wraps
from Main import app, db
from flask import render_template, request, redirect, session, flash, url_for
from controllers.validations import validar_documento
from forms.form_user import FormUser
from forms.form_login import FormLogin
from models_DB.companies import Companies
from models_DB.users import UsersDb
from werkzeug.security import generate_password_hash, check_password_hash


# decorador que verifica se o usuario está logado em outras sessoes
# ao chamar uma url que deve ser verificada, colocar o decorador login_required acima da função

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Você precisa fazer login para acessar esta página.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function  


# rota de cadastro 
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = FormUser()
    titulo = 'Cadastro'

    # seleciona as distriuidoras cadastradas
    distribuidoras = Companies.query.all()
    form.distribuidora.choices = [(str(d.id), d.nome_distribuidora) for d in distribuidoras]

    # o tipo de pessoa fisica ou juridica vai ser selecionado direto do form

    if form.validate_on_submit():  # valida todos os validators nativos
        # Validação customizada externa
        erros = validar_documento(
            tipo_documento=form.tipo_documento.data,
            cpf=form.cpf.data,
            nome_fantasia=form.nome_fantasia.data
        )

        if erros:
            for campo, msg in erros.items():
                getattr(form, campo).errors.append(msg)
            return render_template('Cadastro.html', titulo=titulo, form=form)

        # Preparando dados para salvar
        nome = form.nome.data
        tipo_usuario = int(form.tipo_usuario.data)
        email = form.email.data
        senha = generate_password_hash(form.senha.data)

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

        # Verifica se o e-mail já existe
        if UsersDb.query.filter_by(email=email).first():
            flash('O e-mail informado já está em uso. Por favor, utilize outro e-mail.', 'danger')
            return render_template('Cadastro.html', titulo=titulo, form=form)

        # cria o novo usuário
        novo_usuario = UsersDb(
            nome=nome,
            id_tipo=tipo_usuario,
            email=email,
            senha=senha,
            documento=documento,
            razao_social=razao_social,
            cep=cep,
            numero=numero,
            telefone=telefone,
            id_distribuidora=id_distribuidora
        )

        db.session.add(novo_usuario)
        db.session.commit()
        flash('Usuário cadastrado com sucesso!', 'success')

        return redirect(url_for('bugig'))

    return render_template('Cadastro.html', titulo=titulo, form=form)


#aqui será a tela principal do sistema, onde o cliente é redirecionado após logar.
@app.route('/bugig')
@login_required
def bugig():

    return render_template('bugig.html')


# rota de login 
@app.route('/login', methods=['POST', 'GET'])
def login():

    form = FormLogin()
    titulo = 'Login'

    if form.validate_on_submit():

        email = form.email.data
        usuario = UsersDb.query.filter_by(email=email).first()

        if usuario and check_password_hash(usuario.senha, form.senha.data):
            
            # cria a session do ususário que será utilizada para validações de rotas
            session['user_id'] = usuario.id
            session['user_nome'] = usuario.nome
            session['user_tipo'] = usuario.id_tipo

            flash(f'Login efetuado com sucesso. Seja bem vindo!', 'success')
            return redirect(url_for('bugig'))
        else:

            flash('Email ou senha inválidos!', 'danger')
            return render_template('login.html', titulo=titulo, form=form)
        
    return render_template('login.html', titulo=titulo, form=form)
