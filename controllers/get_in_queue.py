from . import auth_bp
from flask import render_template, redirect, url_for
from controllers.login import user_owns_resource
from forms.form_queue import FormQueue
from models_DB.companies import Companies


@auth_bp.route('/<int:user_id>/get-in-queue', methods=['POST', 'GET']) # função de entrar na fila
@user_owns_resource('user_id', tipo_usuario_esperado=1) # só o beneficiário pode acessar
def get_in_queue(user_id):
    titulo = 'Entrar na Fila'
    form_queue = FormQueue()
    form_queue.distribuidora.choices = [str((d.id, d.nome_distribuidora)) for d in Companies.query.all()]
    # seleciona todas as distribuidoras cadastradas no banco

    if form_queue.validate_on_submit():
        qtd = form_queue.qtd_solicitada.data
        distribuidora_id = form_queue.distribuidora.data

        print(f'Sua solicitação de {qtd} unidades para a distribuidora {distribuidora_id} foi realizada com sucesso.')
        return redirect(url_for('auth.menu_benef')) # após entrar na fila retorna para a tela de menu principal
    return render_template('queue.html', form_queue=form_queue, user_id=user_id, titulo=titulo)
