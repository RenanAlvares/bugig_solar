from extensions import db
from flask import render_template, redirect, url_for, flash, request
from controllers.login import user_owns_resource
from . import auth_bp
from forms.form_user import FormUser
from models_DB.companies import Companies
from models_DB.users import UsersDb
from werkzeug.security import check_password_hash as check_password

@auth_bp.route('/<int:user_id>/edit-user', methods=['GET', 'POST'])
@user_owns_resource('user_id')
def edit_user(user_id):
    usuario = UsersDb.query.get_or_404(user_id)

    # --- definições de choices iguais às do cadastro ---
    tipo_usuario_choices = [('1', 'Beneficiário'), ('2', 'Gerador')]
    tipo_documento_choices = [('cpf', 'CPF'), ('cnpj', 'CNPJ')]

    # distribuidoras (sempre definir)
    distribuidoras = Companies.query.all()
    distrib_choices = [(str(d.id), d.nome_distribuidora) for d in distribuidoras]

    # --- instanciação do form: POST vs GET ---
    if request.method == 'POST':
        # cria o form a partir dos dados submetidos (para que validate_on_submit leia request.form)
        form = FormUser(request.form)
        # assegura choices mesmo no POST (necessário para validação/render)
        form.tipo_usuario.choices = tipo_usuario_choices
        form.tipo_documento.choices = tipo_documento_choices
        form.distribuidora.choices = distrib_choices
        
        # CRÍTICO: Na edição, os campos desabilitados não vêm no request.form
        # Então precisamos forçar os valores do banco para passar na validação
        form.tipo_usuario.data = str(usuario.id_tipo_user)
        form.tipo_documento.data = 'cpf' if getattr(usuario, 'id_tipo_pessoa', None) == 1 else 'cnpj'
        
    else:
        # GET: pré-carrega com os dados do usuário
        form = FormUser(obj=usuario)
        form.tipo_usuario.choices = tipo_usuario_choices
        form.tipo_documento.choices = tipo_documento_choices
        form.distribuidora.choices = distrib_choices

        # garante que os dados estejam no formato esperado (strings)
        form.tipo_usuario.data = str(usuario.id_tipo_user) if usuario.id_tipo_user is not None else ''
        form.tipo_documento.data = 'cpf' if getattr(usuario, 'id_tipo_pessoa', None) == 1 else 'cnpj'
        form.distribuidora.data = str(getattr(usuario, 'id_distribuidora', '') or '')

        # preencher campo de documento correto no form (apenas pra exibir)
        if form.tipo_documento.data == 'cpf':
            form.cpf.data = usuario.documento
        else:
            form.cnpj.data = usuario.documento

        # nome fantasia / razao social (se houver)
        form.nome_fantasia.data = getattr(usuario, 'razao_social', '')

    # --- processamento do POST ---
    if form.validate_on_submit():
        # confirma senha ANTES de processar
        confirm_pwd = form.confirm_senha.data
        if not confirm_pwd:
            flash('Por favor, digite sua senha para confirmar as alterações!', 'danger')
            return render_template('edit_user.html', form=form, titulo="Editar Cadastro", user_id=user_id, usuario=usuario)
            
        if not check_password(usuario.senha, confirm_pwd):
            flash('Senha incorreta para confirmar alterações!', 'danger')
            return render_template('edit_user.html', form=form, titulo="Editar Cadastro", user_id=user_id, usuario=usuario)

        # Atualiza só os campos permitidos (NÃO altera tipo de usuário / tipo documento / documento)
        usuario.nome = form.nome.data
        usuario.email = form.email.data
        usuario.telefone = form.telefone.data
        usuario.cep = form.cep.data
        usuario.numero = form.numero.data

        # distribuidora (se fornecida)
        try:
            if form.distribuidora.data:
                usuario.id_distribuidora = int(form.distribuidora.data)
        except ValueError:
            pass

        # nome fantasia (apenas se for pessoa jurídica)
        if getattr(usuario, 'id_tipo_pessoa', None) == 2:
            usuario.razao_social = form.nome_fantasia.data

        # NÃO sobrescrever usuario.documento / id_tipo_pessoa / id_tipo_user
        # Commit
        try:
            db.session.commit()
            flash('Dados atualizados com sucesso!', 'success')
            return redirect(url_for('auth.menu_benef', user_id=user_id) if usuario.id_tipo_user == 1 else url_for('auth.menu_gen', user_id=user_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar usuário: {str(e)}', 'danger')
    else:
        # DEBUG: Mostrar erros de validação
        if request.method == 'POST' and form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Erro no campo {field}: {error}', 'danger')

    # render (GET ou validação falhou)
    return render_template('edit_user.html', form=form, titulo="Editar Cadastro", user_id=user_id, usuario=usuario)