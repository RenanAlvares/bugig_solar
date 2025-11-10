from extensions import db
from flask import render_template, redirect, url_for, flash, request, current_app
from controllers.login import user_owns_resource
from . import auth_bp
from forms.form_user import FormUser
from models_DB.companies import Companies
from models_DB.users import UsersDb
from werkzeug.security import check_password_hash as check_password
import os
from time import time

import os
from flask import url_for, current_app

def get_user_photo_url(user_id):
    """
    Busca a foto de perfil do usuário no sistema de arquivos.
    Retorna a URL da foto ou None se não encontrada.
    """
    folder = current_app.config.get('UPLOAD_FOLDER', os.path.join('static', 'uploads', 'fotos_perfil'))
    
    if not os.path.exists(folder):
        return None
    
    # Busca arquivos que começam com user_{id}_
    fotos = [f for f in os.listdir(folder) if f.startswith(f'user_{user_id}_')]
    
    if fotos:
        # Retorna a foto mais recente (última modificação)
        foto_mais_recente = max(fotos, key=lambda f: os.path.getmtime(os.path.join(folder, f)))
        return url_for('static', filename=f'uploads/fotos_perfil/{foto_mais_recente}')
    
    return None

@auth_bp.route('/<int:user_id>/edit-user', methods=['GET', 'POST'])
@user_owns_resource('user_id')
def edit_user(user_id):
    usuario = UsersDb.query.get_or_404(user_id)

    tipo_usuario_choices = [('1', 'Beneficiário'), ('2', 'Gerador')]
    tipo_documento_choices = [('cpf', 'CPF'), ('cnpj', 'CNPJ')]
    foto_url = get_user_photo_url(user_id)

    distribuidoras = Companies.query.all()
    distrib_choices = [(str(d.id), d.nome_distribuidora) for d in distribuidoras]

    if request.method == 'POST':
        form = FormUser(request.form)
        form.tipo_usuario.choices = tipo_usuario_choices
        form.tipo_documento.choices = tipo_documento_choices
        form.distribuidora.choices = distrib_choices
        
        form.tipo_usuario.data = str(usuario.id_tipo_user)
        form.tipo_documento.data = 'cpf' if getattr(usuario, 'id_tipo_pessoa', None) == 1 else 'cnpj'
        
    else:
        form = FormUser(obj=usuario)
        form.tipo_usuario.choices = tipo_usuario_choices
        form.tipo_documento.choices = tipo_documento_choices
        form.distribuidora.choices = distrib_choices

        form.tipo_usuario.data = str(usuario.id_tipo_user) if usuario.id_tipo_user is not None else ''
        form.tipo_documento.data = 'cpf' if getattr(usuario, 'id_tipo_pessoa', None) == 1 else 'cnpj'
        form.distribuidora.data = str(getattr(usuario, 'id_distribuidora', '') or '')

        if form.tipo_documento.data == 'cpf':
            form.cpf.data = usuario.documento
        else:
            form.cnpj.data = usuario.documento

        form.nome_fantasia.data = getattr(usuario, 'razao_social', '')

    if form.validate_on_submit():
        confirm_pwd = form.confirm_senha.data
        if not confirm_pwd:
            flash('Por favor, digite sua senha para confirmar as alterações!', 'danger')
            return render_template('edit_user.html', form=form, titulo="Editar Cadastro", user_id=user_id, usuario=usuario)
            
        if not check_password(usuario.senha, confirm_pwd):
            flash('Senha incorreta para confirmar alterações!', 'danger')
            return render_template('edit_user.html', form=form, titulo="Editar Cadastro", user_id=user_id, usuario=usuario)

        # atualiza somente os campos permitidos
        usuario.nome = form.nome.data
        usuario.email = form.email.data
        usuario.telefone = form.telefone.data
        usuario.cep = form.cep.data
        usuario.numero = form.numero.data

        try:
            if form.distribuidora.data:
                usuario.id_distribuidora = int(form.distribuidora.data)
        except ValueError:
            pass

        if getattr(usuario, 'id_tipo_pessoa', None) == 2:
            usuario.razao_social = form.nome_fantasia.data

        arquivo = request.files.get('foto_perfil')
        remover_foto = request.form.get('remover_foto') == '1'

        folder = current_app.config.get('UPLOAD_FOLDER', os.path.join('static', 'uploads', 'fotos_perfil'))
        if not os.path.exists(folder):
            os.makedirs(folder)

        # valida se o usuário removeu a foto
        if remover_foto:
            fotos_antigas = [f for f in os.listdir(folder) if f.startswith(f'user_{user_id}_')]
            for foto_antiga in fotos_antigas:
                try:
                    os.remove(os.path.join(folder, foto_antiga))
                except Exception as e:
                    print(f"⚠️ Erro ao remover foto antiga: {e}")

        elif arquivo and arquivo.filename != '':
            filename = arquivo.filename
            extensao = filename.rsplit('.', 1)[-1].lower()

            if extensao not in {'png', 'jpg', 'jpeg'}:
                flash('Formato de imagem inválido. Envie PNG, JPG ou JPEG.', 'danger')
                return render_template('edit_user.html', form=form, titulo="Editar Cadastro", user_id=user_id, usuario=usuario)

            # remove foto antiga antes de salvar nova
            fotos_antigas = [f for f in os.listdir(folder) if f.startswith(f'user_{user_id}_')]
            for foto_antiga in fotos_antigas:
                try:
                    os.remove(os.path.join(folder, foto_antiga))
                except Exception as e:
                    print(f"⚠️ Erro ao remover foto antiga: {e}")

            # salva nova foto
            momento = int(time())
            nome_final = f"user_{user_id}_{momento}.{extensao}"
            caminho_arquivo = os.path.join(folder, nome_final)

            try:
                arquivo.save(caminho_arquivo)
            except Exception as e:
                flash(f'Erro ao salvar foto: {str(e)}', 'warning')

        # commit no banco
        try:
            db.session.commit()
            flash('Dados atualizados com sucesso!', 'success')
            return redirect(url_for('auth.menu_benef', user_id=user_id) if usuario.id_tipo_user == 1 else url_for('auth.menu_gen', user_id=user_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar usuário: {str(e)}', 'danger')
    else:
        # mostrar erros de validação se houver
        if request.method == 'POST' and form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Erro no campo {field}: {error}', 'danger')

    return render_template(
        'edit_user.html', 
        form=form, 
        titulo="Editar Cadastro",
        user_id=user_id,
        usuario=usuario,
        foto_url=foto_url
    )
