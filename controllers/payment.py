from extensions import db
from forms.form_payment import Payment as FormPayment
from flask import render_template, redirect, send_file, url_for, flash, abort, session
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
import io
import csv


def gerar_csv_pagamento(user_id, pagamento_id):
    """Função auxiliar para gerar o CSV do comprovante de pagamento"""
    
    # Busca o pagamento com validação de permissão
    pagamento = Payment.query.get_or_404(pagamento_id)
    
    # Verifica se o pagamento pertence ao usuário
    benef = Beneficiaries.query.filter_by(id_user=user_id).first_or_404()
    
    # Valida se o pagamento está relacionado ao beneficiário
    if pagamento.transferencia.user_fila.id_beneficiario != benef.id:
        abort(403)  # Forbidden

    # Criar buffer de texto para o CSV
    output = io.StringIO()
    writer = csv.writer(output, delimiter=';', quoting=csv.QUOTE_MINIMAL)

    # Cabeçalho do relatório
    writer.writerow(['COMPROVANTE DE PAGAMENTO'])
    writer.writerow([f'Data de Emissão: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}'])
    writer.writerow([])  # Linha em branco

    # dados do Beneficiário
    usuario = UsersDb.query.get(user_id)
    writer.writerow(['DADOS DO BENEFICIÁRIO'])
    writer.writerow(['Nome', usuario.nome])
    writer.writerow(['Documento', usuario.documento])
    writer.writerow([])  # Linha em branco

    # Dados do Pagamento
    writer.writerow(['DADOS DO PAGAMENTO'])
    writer.writerow(['ID do Pagamento', pagamento.id])
    writer.writerow(['Tipo de Pagamento', pagamento.tipo_pagamento.nome_tipo])
    writer.writerow(['Data de Emissão', pagamento.data_emissao.strftime('%d/%m/%Y %H:%M:%S')])
    writer.writerow(['Data de Liquidação', pagamento.data_liquidacao.strftime('%d/%m/%Y %H:%M:%S')])
    writer.writerow([])  # Linha em branco

    # Dados da Transferência
    qtd_creditos = pagamento.transferencia.user_fila.quantidade_recebida or 0
    valor_total = qtd_creditos * 0.90
    
    writer.writerow(['DADOS DA TRANSFERÊNCIA'])
    writer.writerow(['Quantidade de Créditos (KWh)', qtd_creditos])
    writer.writerow(['Valor por KWh (R$)', '0,10'])
    writer.writerow(['Valor Total Economizado (R$)', f'{valor_total:.2f}'])
    writer.writerow([])  # Linha em branco

    # Rodapé
    writer.writerow(['Este documento serve como comprovante de pagamento de créditos de energia solar.'])

    # Preparar o arquivo para download
    output.seek(0)
    
    # Converter StringIO para BytesIO com encoding UTF-8 + BOM (para Excel)
    csv_bytes = io.BytesIO()
    csv_bytes.write('\ufeff'.encode('utf-8'))  # BOM para UTF-8
    csv_bytes.write(output.getvalue().encode('utf-8'))
    csv_bytes.seek(0)

    return csv_bytes


@auth_bp.route('/<int:user_id>/download-payment-csv/<int:pagamento_id>', methods=['GET'])
@user_owns_resource('user_id', tipo_usuario_esperado=1)
def download_payment_csv(user_id, pagamento_id):
    """Rota para download do CSV (pode ser usado para baixar novamente)"""
    
    csv_bytes = gerar_csv_pagamento(user_id, pagamento_id)
    
    return send_file(
        csv_bytes,
        as_attachment=True,
        download_name=f'comprovante_pagamento_{pagamento_id}_{datetime.now().strftime("%Y%m%d_%H%M")}.csv',
        mimetype='text/csv'
    )


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
                
                # salva o ID do pagamento na sessão para exibir link de download
                session['ultimo_pagamento_id'] = pagamento.id
                
                flash('Pagamento realizado com sucesso!', 'success')
                return redirect(url_for('auth.menu_benef', user_id=user_id))
                
            except Exception as e:
                db.session.rollback()
                flash('Erro ao realizar o pagamento. Tente novamente.', 'danger')
                return redirect(url_for('auth.menu_benef', user_id=user_id))
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