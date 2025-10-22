from models_DB.benef_gen import Beneficiaries
from models_DB.donation_queue import Donation, Queue
from extensions import db
from models_DB.transfer import Transfer
from models_DB.payments import Payment 
from datetime import datetime, timedelta
from models_DB.users import UsersDb as Usuarios  # alterei para usuarios pq fiz a funcao com esse nome

def valida_mes_fila_doacao():

    mes_atual, ano_atual = datetime.now().month, datetime.now().year
    doacoes = Donation.query.filter_by(status=1).all()

    for doacao in doacoes:
        if (doacao.data_doacao.year, doacao.data_doacao.month) != (ano_atual, mes_atual):
            doacao.status = 0 # expirou a dooacao daquele mes

    filas = Queue.query.filter_by(status=1).all()

    for fila in filas:
        if (fila.data_solicitacao.year, fila.data_solicitacao.month) != (ano_atual, mes_atual):
            fila.status = 0 # expirou a fila daquele mes

    db.session.commit()

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
    db.session.commit()


def transfer():
    # busca todas as doações ativas ordenadas pela data da doação
    valida_mes_fila_doacao()
    doacoes = Donation.query.filter_by(status=1).order_by(Donation.data_doacao.asc()).all()

    # se não houver nenhuma doação ativa, encerra
    if not doacoes:
        return

    for doacao in doacoes:
        # pega a distribuidora do gerador que fez a doação
        gen_distribuidora = doacao.gerador.usuario.id_distribuidora

        # busca a fila compatível (mesma distribuidora)
        fila = (
            Queue.query
            .join(Beneficiaries, Beneficiaries.id == Queue.id_beneficiario)
            .join(Usuarios, Usuarios.id == Beneficiaries.id_user)
            .filter(
                Queue.status == 1,
                Usuarios.id_distribuidora == gen_distribuidora
            )
            .order_by(Queue.data_solicitacao.asc())
            .first()
        )

        # se não houver fila compatível, passa para a próxima doação
        if not fila:
            continue

        # calcula a quantidade transferida (mínimo entre disponível e solicitada restante)
        qtd_transferencia = min(
            doacao.quantidade_disponivel,
            fila.quantidade_solicitada - fila.quantidade_recebida
        )

        # atualiza a quantidade disponível da doação
        doacao.quantidade_disponivel -= qtd_transferencia

        # atualiza a fila
        fila.quantidade_recebida += qtd_transferencia
        if fila.quantidade_recebida >= fila.quantidade_solicitada:
            fila.status = 0  # fila completa

        # atualiza o status da doação se esgotou
        if doacao.quantidade_disponivel <= 0:
            doacao.status = 0

        # cria o registro da transferência
        transferencia = Transfer(
            id_fila=fila.id,
            id_doador=doacao.id,
            data_transferencia=datetime.now(),
            quantidade_transferencia=qtd_transferencia
        )

        db.session.add(transferencia)
        db.session.commit()

        # cria o pagamento associado à transferência
        create_payment_per_transfer(transferencia)
