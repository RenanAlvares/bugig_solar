from datetime import datetime
from . import auth_bp
from flask import render_template, redirect, url_for
from controllers.login import user_owns_resource
from forms.form_queue import FormQueue
from models_DB.donation_queue import Queue
from models_DB.benef_gen import Beneficiaries
from extensions import db


# funcao e validacao que verifica se o usuário já doou este mês
'''def usuario_ja_doou_mes(id_user_doacao):
    
    doacao = Queue.query.filter_by(id_user_doacao=id_user_doacao).order_by(Queue.data_doacao.desc()).first()
    if doacao and doacao.data_doacao.month == datetime.now().month:
        return True
    return False'''


@auth_bp.route('/<int:user_id>/get-in-queue', methods=['POST', 'GET']) # função de entrar na fila
@user_owns_resource('user_id', tipo_usuario_esperado=1) # só o beneficiário pode acessar
def get_in_queue(user_id):
    titulo = 'Entrar na Fila'
    form_queue = FormQueue()
    # seleciona todas as distribuidoras cadastradas no banco

    if form_queue.validate_on_submit():
        qtd = form_queue.qtd_solicitada.data
        benef = Beneficiaries.query.filter_by(id_user=user_id).first()
        id_user_doacao = benef.id
        qtd_max = benef.consumo_mensal

        if qtd > qtd_max:
            form_queue.qtd_solicitada.errors.append(f'A quantidade solicitada não pode ser maior que o seu consumo mensal ({qtd_max} kWh).')
            return render_template('queue.html', form_queue=form_queue, user_id=user_id, titulo=titulo)

        # funcao e validacao que verifica se o usuário já doou este mês
        # deixei comentado para realizar testes 
        '''if usuario_ja_doou_mes(id_user_doacao):
            form_queue.qtd_solicitada.errors.append('Você já entrou na fila este mês. Só é possível entrar uma vez por mês.')
            return render_template('queue.html', form_queue=form_queue, user_id=user_id, titulo=titulo)'''

        entrar_fila = Queue(
            id_beneficiario=id_user_doacao,
            quantidade_solicitada=qtd,
            data_solicitacao=datetime.now().date(),
            status=True,
            quantidade_recebida=0
        )
        db.session.add(entrar_fila)
        db.session.commit()
        # após entrar na fila, redireciona para a tela de menu principal

        return redirect(url_for('auth.menu_benef', user_id=user_id)) # após entrar na fila retorna para a tela de menu principal
    return render_template('queue.html', form_queue=form_queue, user_id=user_id, titulo=titulo)
