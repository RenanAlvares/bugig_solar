from . import auth_bp
from flask import render_template, redirect, send_file, url_for
from .login import user_owns_resource
from models_DB.donation_queue import Queue, Donation
from models_DB.benef_gen import Beneficiaries, Generators
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
import matplotlib.pyplot as plt
from reportlab.platypus import Table, TableStyle, Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime
from reportlab.lib.styles import getSampleStyleSheet
import io

# funcao que gera o relatorio do beneficiario
@auth_bp.route('/<int:user_id>/report-benef', methods=['GET'])
@user_owns_resource('user_id', tipo_usuario_esperado=1)
def report_benef(user_id):

    titulo = 'Relatório do Beneficiário'

    #busca o id do beneficiario associado ao user_id
    id_beneficiario = Beneficiaries.query.filter_by(id_user=user_id).first().id

    # seleciona todas as acoes desse beneficiario
    fila = Queue.query.filter_by(id_beneficiario=id_beneficiario).order_by(Queue.data_solicitacao.desc()).all()

    return render_template('reports.html', user_id=user_id, fila=fila, titulo=titulo)


# funcao que gera o pdf do relatorio (beneficiario ou gerador)
@auth_bp.route('/<int:user_id>/download-report')
@user_owns_resource('user_id')
def download_report(user_id):

    user = Beneficiaries.query.filter_by(id_user=user_id).first()
    
    tipo_usuario = 1  if user else 2  # 1 = Beneficiário, 2 = Gerador

    """
    Gera um relatório em PDF com tabela de movimentações da fila
    (sem gráfico), com o tema amarelo e preto futurista.
    """

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()

    # ====== ESTILOS PERSONALIZADOS ======
    titulo_style = ParagraphStyle(
        'Titulo',
        parent=styles['Heading1'],
        textColor="#F2B705",
        alignment=1,
        fontSize=20,
        spaceAfter=20,
    )

    normal_style = ParagraphStyle(
        'NormalCustom',
        parent=styles['Normal'],
        textColor="#111",
        fontSize=11,
        leading=16,
    )

    # ====== CABEÇALHO ======
    titulo = "Relatório do Beneficiário" if tipo_usuario == 1 else "Relatório do Gerador"

    elements = [
        Paragraph(f"<b>{titulo}</b>", titulo_style),
        Spacer(1, 0.3 * cm),
        Paragraph(f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M')}", normal_style),
        Spacer(1, 0.8 * cm),
    ]

    # ====== CONSULTA DE DADOS ======
    if tipo_usuario == 1:
        fila = Queue.query.filter_by(id_beneficiario=user.id).all()
    else:
        user = Generators.query.filter_by(id_user=user_id).first()
        fila = Queue.query.filter_by(id_beneficiario=user.id).all()  # ajuste se gerador usar outra FK

    if not fila:
        elements.append(Paragraph("Nenhum registro encontrado na sua fila.", normal_style))
    else:
        # Cabeçalho da tabela
        data = [["Data", "Créditos Recebidos (kWh)", "Valor Economizado (R$)", "Status"]]

        for posicao in fila:
            data_solic = posicao.data_solicitacao.strftime("%d/%m/%Y") if posicao.data_solicitacao else "—"
            creditos = posicao.quantidade_recebida or 0
            valor = f"R$ {creditos * 0.95:.2f}" if creditos else "—"
            status_text = "Concluído" if posicao.status == 0 else "Pendente"
            status_color = colors.green if posicao.status == 0 else colors.red

            data.append([data_solic, creditos, valor, status_text])

        # ====== ESTILO DA TABELA ======
        tabela = Table(data, colWidths=[4 * cm, 5 * cm, 5 * cm, 4 * cm])

        estilo_tabela = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.95, 0.72, 0.02)),  # amarelo
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('BOX', (0, 0), (-1, -1), 1, colors.gray),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.gray),
        ])

        tabela.setStyle(estilo_tabela)

        # Aplica cor verde/vermelha nas células de status
        for i, posicao in enumerate(fila, start=1):
            cor = colors.green if posicao.status == 0 else colors.red
            estilo_tabela.add('TEXTCOLOR', (-1, i), (-1, i), cor)

        tabela.setStyle(estilo_tabela)

        elements.append(tabela)

    # ====== GERA O PDF ======
    doc.build(elements)

    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"relatorio_{tipo_usuario}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
        mimetype='application/pdf'
    )