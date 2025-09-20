from Main import app, auth_bp
from flask import Blueprint, render_template, request, redirect, session, flash, url_for, send_from_directory
from controllers.login import login_required
from forms.form_queue import FormQueue
from models_DB.companies import DistribuidoraModel


@auth_bp.route('/get-in-queue', methods=['POST', 'GET']) # função de entrar na fila
@login_required
def get_in_queue():

    form = FormQueue()
    form.distribuidora.choices = [(d.id_distribuidora, d.nome_distribuidora) for d in DistribuidoraModel.query.all()]
    # seleciona todas as distribuidoras cadastradas no banco

    if form.validate_on_submit():
        qtd = form.qtd_solicitada.data
        distribuidora_id = form.distribuidora.data

        print(f'Sua solicitação de {qtd} unidades para a distribuidora {distribuidora_id} foi realizada com sucesso.')
        return redirect(url_for('bugig')) # após entrar na fila retorna para a tela de menu principal
    return render_template('about.html', form=form) # depois q tiver a tela de fila, mudar o template
