from functools import wraps
from extensions import db
from flask import Blueprint, render_template, redirect, session, flash, url_for
from controllers.validations import validar_documento
from forms.form_benef import FormBenef
from forms.form_gen import FormGen
from forms.form_user import FormUser
from forms.form_login import FormLogin
from models_DB.benef_gen import Beneficiaries, Generators
from models_DB.companies import Companies
from models_DB.types import TipoClasses, TipoGeracao
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
    form_benef.classe_consumo.choices = [(str(c.id_tipo_classe), c.nome_tipo_classe) for c in TipoClasses.query.all()]
    form_gen.id_tipo_geracao.choices = [(str(g.id_tipo_geracao), g.nome_tipo_geracao) for g in TipoGeracao.query.all()]

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

       # criar cadastro do beneficiario
        if tipo_usuario == 1:  # Beneficiário
            consumo_mensal = form_benef.consumo_mensal.data
            classe_consumo = int(form_benef.classe_consumo.data)

            # cria o beneficiario   
            novo_beneficiario = Beneficiaries(
                consumo_mensal=consumo_mensal,
                id_tipo_classe=classe_consumo,
                id_usuario=novo_usuario.id
            )

            db.session.add(novo_beneficiario)
            db.session.commit()
            flash('Beneficiário cadastrado com sucesso!', 'success')

        # criar cadastro do gerador
        elif tipo_usuario == 2:  # Gerador
            producao_mensal = form_gen.producao_mensal.data
            inicio_operacao = form_gen.inicio_operacao.data
            tipo_geracao = int(form_gen.id_tipo_geracao.data)

            # cria o gerador
            novo_gerador = Generators(
                producao_mensal=producao_mensal,
                inicio_operacao=inicio_operacao,
                id_tipo_geracao=tipo_geracao,
                id_usuario=novo_usuario.id
            )

            db.session.add(novo_gerador)
            db.session.commit()
            flash('Gerador cadastrado com sucesso!', 'success')



        return redirect(url_for('public.landing_page')) # mudar para auth.bugig quando houver o template

    return render_template('Cadastro.html', titulo=titulo, form=form)

@auth_bp.route('/bugig')
@login_required
def bugig():
    return render_template('bugig.html')

# rota de login 
@auth_bp.route('/login', methods=['POST', 'GET'])
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
            return redirect(url_for('auth.bugig'))
        else:

            flash('Email ou senha inválidos!', 'danger')
            return render_template('login.html', titulo=titulo, form=form)
        
    return render_template('login.html', titulo=titulo, form=form)
