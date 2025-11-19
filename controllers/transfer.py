from models_DB.benef_gen import Beneficiaries
from models_DB.donation_queue import Donation, Queue
from extensions import db
from models_DB.transfer import Transfer
from models_DB.payments import Payment 
from datetime import datetime, timedelta
from models_DB.users import UsersDb as Usuarios  # alterei para usuarios pq fiz a funcao com esse nome

def valida_mes_fila_doacao():

    mes_atual, ano_atual = datetime.now().month, datetime.now().year
    doacoes = Donation.query.filter_by(status=True).all()

    for doacao in doacoes:
        if (doacao.data_doacao.year, doacao.data_doacao.month) != (ano_atual, mes_atual):
            doacao.status = False # expirou a dooacao daquele mes

    filas = Queue.query.filter_by(status=True).all()

    for fila in filas:
        if (fila.data_solicitacao.year, fila.data_solicitacao.month) != (ano_atual, mes_atual):
            fila.status = False # expirou a fila daquele mes

    db.session.flush()

# aqui será criado o pagamento parcial para cada transferencia realizada
def create_payment_per_transfer(transfer: Transfer):

    vencimento = datetime.now() + timedelta(days=7)

    pagamento = Payment(
        id_transferencia=transfer.id,
        data_emissao=datetime.now(),
        id_tipo_pagamento=4,  # 4 pois esse campo é not null e o beneficiario vai alterar ao realizar o pagamento
        data_vencimento=vencimento,
        data_liquidacao=None,
        valor=transfer.quantidade_transferencia * 0.1  # já é definido 10 centavos por crédito
    )

    db.session.add(pagamento)


def transfer():
    valida_mes_fila_doacao()
    doacoes = Donation.query.filter_by(status=True).order_by(Donation.data_doacao.asc()).all()

    if not doacoes:
        return

    for doacao in doacoes:
        gen_distribuidora = doacao.gerador.usuario.id_distribuidora

        fila = (
            Queue.query
            .join(Beneficiaries, Beneficiaries.id == Queue.id_beneficiario)
            .join(Usuarios, Usuarios.id == Beneficiaries.id_user)
            .filter(
                Queue.status == True,
                Usuarios.id_distribuidora == gen_distribuidora
            )
            .order_by(Queue.data_solicitacao.asc())
            .first()
        )

        if not fila:
            continue

        qtd_transferencia = int(min(
            doacao.quantidade_disponivel,
            fila.quantidade_solicitada - fila.quantidade_recebida
        ))

        # Atualiza a doação
        doacao.quantidade_disponivel -= qtd_transferencia
        if doacao.quantidade_disponivel <= 0:
            doacao.status = False

        # Atualiza a fila
        fila.quantidade_recebida += qtd_transferencia
        if fila.quantidade_recebida >= fila.quantidade_solicitada:
            fila.status = False

        # Cria a transferência
        transferencia = Transfer(
            id_fila=fila.id,
            id_doador=doacao.id,
            data_transferencia=datetime.now(),
            quantidade_transferencia=qtd_transferencia
        )

        db.session.add(transferencia)
        db.session.flush()
        
        create_payment_per_transfer(transferencia)

    # NÃO FAZ COMMIT AQUI - o commit será feito em get_in_queue