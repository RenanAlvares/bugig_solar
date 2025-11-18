from models_DB.donation_queue import Donation
from datetime import datetime
from . import auth_bp
from flask import render_template, redirect, url_for
from controllers.login import user_owns_resource
from forms.form_donation import FormDonation
from models_DB.benef_gen import Generators
from extensions import db
from .transfer import transfer

'''
def usuario_ja_doou(id_user_doacao):
    doacao = Donation.query.filter_by(id_user_doacao=id_user_doacao).order_by(Queue.data_doacao.desc()).first()
    if doacao and doacao.data_doacao.month == datetime.now().month:
        return True
    return False
'''

@auth_bp.route('/<int:user_id>/make-donation', methods=['POST', 'GET']) # função de fazer doação
@user_owns_resource('user_id', tipo_usuario_esperado=2) # só o gerador pode acessar
def make_donation(user_id):

    form_donation = FormDonation()
    titulo = 'Fazer Doação'

    if form_donation.validate_on_submit():

        gen = Generators.query.filter_by(id_user=user_id).first()
        qtd_doada = form_donation.qtd_doada.data
        qtd_max_doacao = gen.producao_mensal_med
        id_gerador = gen.id

        if qtd_doada > qtd_max_doacao:
            form_donation.qtd_doada.errors.append(f'A quantidade a ser doada não pode ser maior que a sua produção mensal ({qtd_max_doacao} kWh).')
            return render_template('make_donation.html', form_donation=form_donation, user_id=user_id, titulo=titulo)
        
        # funcao que valida se o usuario ja doou este mes
        '''if usuario_ja_doou(id_gerador):
            form_donation.qtd_doada.errors.append('Você já fez uma doação este mês. Só é possível doar uma vez por mês.')
            return render_template('make_donation.html', form_donation=form_donation, user_id=user_id, titulo=titulo)'''

        nova_doacao = Donation(
            id_gerador=id_gerador,
            quantidade_doacao=qtd_doada,
            data_doacao=datetime.now(),
            status=True,
            quantidade_disponivel=qtd_doada
        )

        db.session.add(nova_doacao)

        db.session.flush()
        
        transfer() # <- função que faz a consulta se há pendencias para gerar transferencia.

        db.session.commit()

        return redirect(url_for('auth.menu_gen', user_id=user_id)) # após doar retorna para a tela de menu principal

    return render_template('make_donation.html', form_donation=form_donation, user_id=user_id, titulo=titulo)
