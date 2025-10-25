from extensions import db
from forms.form_payment import Payment as FormPayment
from flask import render_template, redirect, url_for, flash
from werkzeug.security import check_password_hash
from models_DB.benef_gen import Beneficiaries
from models_DB.users import UsersDb
from . import auth_bp
from .login import user_owns_resource
from models_DB.types import TipoPagamento
from models_DB.transfer import Transfer
from models_DB.payments import Payment
from datetime import datetime


@auth_bp.route('/<int:user_id>/payment', methods=['GET', 'POST'])
@user_owns_resource('user_id', tipo_usuario_esperado=1)
def payment(user_id):
    form_payment = FormPayment()

    tipo_pagamento = TipoPagamento.query.filter(TipoPagamento.id < 4).all()
    form_payment.tipo_pagamento.choices = [(str(tp.id), tp.nome_tipo) for tp in tipo_pagamento]

    if form_payment.validate_on_submit():

        confirma_senha = form_payment.senha.data
        senha_usuario = UsersDb.query.get(user_id).senha

        if not check_password_hash(senha_usuario, confirma_senha):

            flash('Senha incorreta. Tente novamente.', 'danger')
            return render_template(
                'menu_benef.html', 
                form_payment=int(form_payment), 
                user_id=user_id, 
                titulo='Pagamento',
                tipo_pagamento=tipo_pagamento
                )

        pagamento = (
            Payment.query
            .join(Transfer, Transfer.id == Payment.id_transferencia)
            .filter(
                Transfer.id_fila.isnot(None),
                Transfer.fila.has(Beneficiaries.id_user == user_id),
                Payment.id_tipo_pagamento == 4
            )
            .first()
        )
        if not pagamento:
            flash('Nenhum pagamento pendente encontrado.', 'warning')
            return redirect(url_for('auth.menu_benef', user_id=user_id))

        pagamento.id_tipo_pagamento = form_payment.tipo_pagamento.data
        pagamento.data_liquidacao = datetime.now()
        db.session.commit()
                
        # Process payment
        flash('Pagamento realizado com sucesso!', 'success')
        return redirect(url_for('auth.menu_benef', user_id=user_id))
    
    return render_template(
        'menu_benef.html', 
        form_payment=form_payment, 
        user_id=user_id, 
        titulo='Pagamento',
        tipo_pagamento=tipo_pagamento
        )