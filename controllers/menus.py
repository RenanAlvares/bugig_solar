from . import auth_bp
from flask import render_template
from .login import user_owns_resource
from models_DB.payments import Payment
from models_DB.transfer import Transfer
from models_DB.donation_queue import Queue
from models_DB.benef_gen import Beneficiaries
from forms.form_payment import Payment as PaymentForm
from models_DB.types import TipoPagamento
from sqlalchemy import and_, or_



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

    benef = Beneficiaries.query.filter_by(id_user=user_id).first()
    fila_ativa = Queue.query.filter_by(id_beneficiario=benef.id, status=True).first()



    posicao_fila = None
    if fila_ativa:
        posicao_fila = (
            Queue.query.filter(and_(
                    Queue.status == True, or_(
                        Queue.data_solicitacao < fila_ativa.data_solicitacao, and_(
                            Queue.data_solicitacao == fila_ativa.data_solicitacao,
                            Queue.id < fila_ativa.id
                        )
                    )
                )
            ).count()
        ) + 1

    return render_template(
        'menu_benef.html',
        user_id=user_id,
        pagamento_pendente=pagamento_pendente,
        form_payment=PaymentForm(),
        posicao_fila=posicao_fila,
        tipo_pagamento=tipo_pagamento
    )


@auth_bp.route('/<int:user_id>/menu-gen', methods=['GET', 'POST'])
@user_owns_resource('user_id', tipo_usuario_esperado=2)
def menu_gen(user_id):
    return render_template('menu_gen.html', user_id=user_id)