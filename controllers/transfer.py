from models_DB.benef_gen import Beneficiaries
from models_DB.donation_queue import Donation, Queue
from extensions import db
from models_DB.transfer import Transfer
from datetime import datetime
from models_DB.users import UsersDb as Usuarios # fiz o as para deixar de acordo com a funcao

def transfer():

    while True:
        
        doacao = Donation.query.filter_by(status=1).order_by(Donation.data_doacao.asc()).first()
        if not doacao:
            break
        
        # pega a distribuidora do gerador que fez a doacao
        gen_distribuidora   = doacao.gerador.usuario.id_distribuidora

        # filtra a fila somente pela distribuidora do gerador
        fila = Queue.query.join(Beneficiaries, Beneficiaries.id == Queue.id_beneficiario)\
                  .join(Usuarios, Usuarios.id == Beneficiaries.id_user)\
                  .filter(Queue.status==1, Usuarios.id_distribuidora == gen_distribuidora)\
                  .order_by(Queue.data_solicitacao.asc()).first()
        
        if not fila:
            continue

        else:

            # ve o valor disponivel e o solicitado para realizar a transferencia
            qtd_transferencia = min(doacao.quantidade_disponivel, fila.quantidade_solicitada - fila.quantidade_recebida)
            
            # atualiza a quantidade disponivel na doacao de acordo com a qtd transferida
            doacao.quantidade_disponivel -= qtd_transferencia

            # atualiza o status da fila e a quantidade recebida
            fila.quantidade_recebida += qtd_transferencia
            if fila.quantidade_recebida >= fila.quantidade_solicitada:
                fila.status = 0

            # atualiza o status da doação
            if doacao.quantidade_disponivel <= 0:
                doacao.status = 0

            # cria as transferencias no banco
            transferencia = Transfer(
                id_fila=fila.id,
                id_doador=doacao.id,
                quantidade_transferida=qtd_transferencia,
                data_transferencia=datetime.now()
            )
            db.session.add(transferencia)
            db.session.commit()


    
