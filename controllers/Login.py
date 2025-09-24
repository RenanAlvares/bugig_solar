from functools import wraps
from extensions import db
from flask import Blueprint, render_template, redirect, request, session, flash, url_for
from controllers.validations import validar_documento
from forms.form_benef import FormBenef
from forms.form_gen import FormGen
from forms.form_user import FormUser
from forms.form_login import FormLogin
from models_DB.companies import Companies
from models_DB.users import UsersDb
from werkzeug.security import generate_password_hash, check_password_hash

# isso faz com que toda rota que tiver auth_bp terá o /bugig antes da rota principal
auth_bp = Blueprint('auth', __name__)

# decorador que verifica se o usuario está logado em outras sessoes
# ao chamar uma url que deve ser verificada, colocar o decorador login_required acima da função

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Você precisa fazer login para acessar esta página.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function  


# rota de cadastro 
@auth_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    form = FormUser()
    form_benef = FormBenef()
    form_gen = FormGen()
    titulo = 'Cadastro'

    # seleciona as distriuidoras cadastradas
    distribuidoras = Companies.query.all()
    form.distribuidora.choices = [(str(d.id), d.nome_distribuidora) for d in distribuidoras]

    # o tipo de pessoa fisica ou juridica vai ser selecionado direto do form

    if form.validate_on_submit():  # valida todos os validators nativos (diferentes dos que estão nos forms)
        # valida o tipo de documento
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
            id_tipo_pessoa = 1  # Fisica
        else:
            documento = form.cnpj.data
            razao_social = form.nome_fantasia.data
            id_tipo_pessoa = 2  # Juridica

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
            id_tipo_user=tipo_usuario,
            email=email,
            senha=senha,
            documento=documento,
            razao_social=razao_social,
            cep=cep,
            numero=numero,
            telefone=telefone,
            id_tipo_pessoa=id_tipo_pessoa,
            id_distribuidora=id_distribuidora
        )

        db.session.add(novo_usuario)
        db.session.commit()
        flash('Usuário cadastrado com sucesso!', 'success')

        # cria a session do ususário que será utilizada para validações de rotas
        session['user_id'] = novo_usuario.id
        session['user_nome'] = novo_usuario.nome

        # armazena o id para salvar no cadastro do beneficiario ou do gerador
        session['new_user_id'] = novo_usuario.id

        if tipo_usuario == 1:  # Beneficiário
            return redirect(url_for('auth.signin_benef'))
        else:  # Gerador
            return redirect(url_for('auth.signin_gen'))


    return render_template('Cadastro.html', titulo=titulo, form=form)

@auth_bp.route('/menu-benef', methods=['GET', 'POST'])
@login_required
def menu_benef():
    return render_template('menu_benef.html')

@auth_bp.route('/menu-gen', methods=['GET', 'POST'])
@login_required
def menu_gen():
    return render_template('menu_gen.html')

# rota de login 
@auth_bp.route('/login', methods=['POST', 'GET'])
def login():

    form = FormLogin()
    titulo = 'Login'

    if form.validate_on_submit():

        email = form.email.data
        usuario = UsersDb.query.filter_by(email=email).first()
        tipo_id = UsersDb.query.filter_by(email=email).first().id_tipo_user

        if usuario and check_password_hash(usuario.senha, form.senha.data):
            
            # cria a session do ususário que será utilizada para validações de rotas
            session['user_id'] = usuario.id
            session['user_nome'] = usuario.nome

            if tipo_id == 1:  # Beneficiário            
                flash(f'Login efetuado com sucesso. Seja bem vindo!', 'success')
                return redirect(url_for('auth.menu_benef'))  # redireciona para a tela principal do sistema
            else:  # Gerador
                flash(f'Login efetuado com sucesso. Seja bem vindo!', 'success')
                return redirect(url_for('auth.menu_gen'))  # redireciona para a tela principal do sistema
        else:

            flash('Email ou senha inválidos!', 'danger')
            return render_template('login.html', titulo=titulo, form=form)
        
    return render_template('login.html', titulo=titulo, form=form)
