from extensions import db
from flask import render_template, redirect, url_for, flash
from controllers.login import user_owns_resource
# A linha "from Main import auth_bp" foi REMOVIDA.
from . import auth_bp
from forms.form_user import FormUser
from models_DB.companies import Companies
from models_DB.users import UsersDb
from werkzeug.security import check_password_hash as check_password

@auth_bp.route('/<int:user_id>/edit-user', methods=['GET', 'POST'])
@user_owns_resource('user_id')  # qualquer tipo pode editar
def edit_user(user_id):
    usuario = UsersDb.query.get_or_404(user_id)
    form = FormUser(obj=usuario)  # pré-carrega os dados

    # Preenche choices da distribuidora
    distribuidoras = Companies.query.all()
    form.distribuidora.choices = [(str(d.id), d.nome_distribuidora) for d in distribuidoras]

    # Bloqueia tipo de usuário para edição
    form.tipo_usuario.render_kw = {'readonly': True}

    if form.validate_on_submit():
        # Valida senha para confirmar alterações
        if not check_password(usuario.senha, form.confirm_senha.data):
            flash('Senha incorreta para confirmar alterações!', 'danger')
            return render_template('edit_user.html', form=form, titulo="Editar Cadastro", user_id=user_id)

        # Atualiza apenas os campos permitidos
        usuario.nome = form.nome.data
        usuario.email = form.email.data
        usuario.telefone = form.telefone.data

        # Atualiza endereço e distribuidora apenas se houver alteração
        endereco_alterado = False
        if usuario.cep != form.cep.data or usuario.numero != form.numero.data:
            endereco_alterado = True
            usuario.cep = form.cep.data
            usuario.numero = form.numero.data
            usuario.id_distribuidora = int(form.distribuidora.data)

        # Atualiza documento se CPF/CNPJ foi alterado
        if form.tipo_documento.data == 'cpf':
            usuario.documento = form.cpf.data
            usuario.razao_social = None
            usuario.id_tipo_pessoa = 1
        else:
            usuario.documento = form.cnpj.data
            usuario.razao_social = form.nome_fantasia.data
            usuario.id_tipo_pessoa = 2

        try:
            db.session.commit()
            flash('Dados atualizados com sucesso!', 'success')
            return redirect(url_for('auth.menu_benef' if usuario.id_tipo_user == 1 else 'auth.menu_gen', user_id=user_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar usuário: {str(e)}', 'danger')

    return render_template('edit_user.html', form=form, titulo="Editar Cadastro", user_id=user_id)