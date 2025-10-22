from flask import render_template, redirect, url_for, flash, request
from . import auth_bp
from controllers.login import user_owns_resource
from models_DB.types import TipoPagamento
from models_DB.payments import Payment
from models_DB.transfer import Transfer
from models_DB.donation_queue import Queue
from models_DB.benef_gen import Beneficiaries
from extensions import db
from datetime import datetime


@auth_bp.route('/<int:user_id>/payment', methods=['POST'])
@user_owns_resource('user_id', tipo_usuario_esperado=1)
def payment(user_id):
    # Tipo de pagamento escolhido no select
    tipo_pagamento = request.form.get('tipo_pagamento')

    # Busca a transferência pendente relacionada ao beneficiário
    transferencia_pendente = (
        Transfer.query
        .join(Queue)
        .join(Beneficiaries, Beneficiaries.id == Queue.id_beneficiario)
        .filter(Beneficiaries.id_user == user_id)
        .order_by(Transfer.data_transferencia.asc())
        .first()
    )

    if not transferencia_pendente:
        flash("Nenhuma transferência pendente encontrada.", "warning")
        return redirect(url_for('auth.menu_benef', user_id=user_id))

    # Cria o pagamento e registra como liquidado
    pagamento = Payment(
        id_transferencia=transferencia_pendente.id,
        id_tipo_pagamento=tipo_pagamento,
        data_emissao=datetime.now(),
        data_liquidacao=datetime.now(),
        valor=transferencia_pendente.valor  # ajusta conforme seu campo no modelo
    )

    db.session.add(pagamento)
    db.session.commit()

    flash("Pagamento realizado com sucesso!", "success")
    return redirect(url_for('auth.menu_benef', user_id=user_id))
