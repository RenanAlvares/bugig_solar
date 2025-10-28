from extensions import db
from forms.form_payment import Payment as FormPayment
from flask import render_template, redirect, url_for, flash
from werkzeug.security import check_password_hash
from models_DB.benef_gen import Beneficiaries
from models_DB.donation_queue import Queue
from models_DB.users import UsersDb
from . import auth_bp
from .login import user_owns_resource
from models_DB.transfer import Transfer
from models_DB.payments import Payment
from datetime import datetime
from models_DB.types import TipoPagamento


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
                form_payment=form_payment,
                user_id=user_id,
                titulo='Pagamento',
                tipo_pagamento=tipo_pagamento
            )

        pagamento = (
            Payment.query
            .join(Payment.transferencia)
            .join(Transfer.user_fila)
            .join(Beneficiaries, Beneficiaries.id == Queue.id_beneficiario)
            .filter(Beneficiaries.id_user == user_id, Payment.data_liquidacao.is_(None))
            .order_by(Payment.data_emissao.asc())
            .first()
        )

        if pagamento:
            pagamento.id_tipo_pagamento = form_payment.tipo_pagamento.data
            pagamento.data_liquidacao = datetime.now()

            try:
                db.session.add(pagamento)
                db.session.commit()
                flash('Pagamento realizado com sucesso!', 'success')
            except Exception:
                db.session.rollback()
                flash('Erro ao realizar o pagamento. Tente novamente.', 'danger')
        else:
            flash('Nenhum pagamento pendente encontrado.', 'warning')

        return redirect(url_for('auth.menu_benef', user_id=user_id))

    return render_template(
        'menu_benef.html',
        form_payment=form_payment,
        user_id=user_id,
        titulo='Pagamento',
        tipo_pagamento=tipo_pagamento
    )
