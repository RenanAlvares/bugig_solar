from . import auth_bp
from flask import render_template
from .login import user_owns_resource
from models_DB.payments import Payment
from models_DB.transfer import Transfer
from models_DB.donation_queue import Queue
from models_DB.benef_gen import Beneficiaries
from forms.form_payment import Payment as PaymentForm
from models_DB.types import TipoPagamento


@auth_bp.route('/<int:user_id>/menu-benef', methods=['GET', 'POST'])
@user_owns_resource('user_id', tipo_usuario_esperado=1)
def menu_benef(user_id):

    tipo_pagamento = TipoPagamento.query.filter(TipoPagamento.id < 4).all()

    # busca o pagamento pendente mais antigo do usuário
    pagamento_pendente = Payment.query \
    .join(Payment.transferencia) \
    .join(Transfer.user_fila) \
    .join(Beneficiaries, Beneficiaries.id == Queue.id_beneficiario) \
    .filter(Beneficiaries.id_user == user_id, Payment.data_liquidacao.is_(None)) \
    .order_by(Payment.data_emissao.asc()) \
    .first()

    return render_template(
        'menu_benef.html',
        user_id=user_id,
        pagamento_pendente=pagamento_pendente,
        form_payment=PaymentForm(),
        tipo_pagamento=tipo_pagamento
    )


@auth_bp.route('/<int:user_id>/menu-gen', methods=['GET', 'POST'])
@user_owns_resource('user_id', tipo_usuario_esperado=2)
def menu_gen(user_id):
    return render_template('menu_gen.html', user_id=user_id)