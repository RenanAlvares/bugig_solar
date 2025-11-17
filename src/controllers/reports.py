from . import auth_bp
from flask import render_template, send_file
from .login import user_owns_resource
from models_DB.donation_queue import Queue, Donation
from models_DB.benef_gen import Beneficiaries, Generators
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet


# =================== RELATÓRIO DO BENEFICIÁRIO ===================
@auth_bp.route('/<int:user_id>/report-benef', methods=['GET'])
@user_owns_resource('user_id', tipo_usuario_esperado=1)
def report_benef(user_id):

    titulo = 'Relatório do Beneficiário'

    id_beneficiario = Beneficiaries.query.filter_by(id_user=user_id).first().id
    fila = Queue.query.filter_by(id_beneficiario=id_beneficiario).order_by(Queue.data_solicitacao.desc()).all()

    return render_template('reports.html', user_id=user_id, fila=fila, titulo=titulo)


# =================== RELATÓRIO DO GERADOR ===================
@auth_bp.route('/<int:user_id>/report-gen', methods=['GET'])
@user_owns_resource('user_id', tipo_usuario_esperado=2)
def report_gen(user_id):

    titulo = 'Relatório do Gerador'

    id_gerador = Generators.query.filter_by(id_user=user_id).first().id
    doacao = Donation.query.filter_by(id_gerador=id_gerador).order_by(Donation.data_doacao.desc()).all()

    return render_template('reports.html', user_id=user_id, doacao=doacao, titulo=titulo)


# =================== DOWNLOAD DO RELATÓRIO (PDF) ===================
@auth_bp.route('/<int:user_id>/download-report')
@user_owns_resource('user_id')
def download_report(user_id):
    from flask import abort
    import io
    from datetime import datetime
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4

    benef = Beneficiaries.query.filter_by(id_user=user_id).first()
    gen = Generators.query.filter_by(id_user=user_id).first()

    if benef:
        tipo_usuario = 1
    elif gen:
        tipo_usuario = 2
    else:
        abort(404)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )
    styles = getSampleStyleSheet()

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
        fontSize=12,
        leading=18,
    )

    titulo = "Relatório do Beneficiário" if tipo_usuario == 1 else "Relatório do Gerador"

    elements = [
        Paragraph(f"<b>{titulo}</b>", titulo_style),
        Spacer(1, 0.5 * cm),
        Paragraph(f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M')}", normal_style),
        Spacer(1, 1.0 * cm),
    ]

    # ========== RELATÓRIO DO BENEFICIÁRIO ==========
    if tipo_usuario == 1:
        fila = Queue.query.filter_by(id_beneficiario=benef.id).order_by(Queue.data_solicitacao.desc()).all()

        if not fila:
            elements.append(Paragraph("Nenhum registro encontrado na sua fila.", normal_style))
        else:
            # ✅ Nova coluna "Quantidade Solicitada"
            data = [
                ["Data", 
                "Quantidade Solicitada", 
                "Créditos Recebidos", 
                "Valor Economizado", 
                "Status"]
            ]

            for pos in fila:
                data_solic = pos.data_solicitacao.strftime("%d/%m/%Y") if pos.data_solicitacao else "—"
                qtd_solicitada = pos.quantidade_solicitada or 0
                qtd_recebida = pos.quantidade_recebida or 0
                valor = f"{qtd_recebida * 0.90:.2f}" if qtd_recebida else "—"
                status_text = "Concluído" if not pos.status else "Pendente"
                data.append([
                    data_solic,
                    f"{qtd_solicitada} KWh",
                    f"{qtd_recebida} KWh",
                    f"{valor} R$",
                    status_text
                ])

            # ✅ Aumentando o espaçamento entre colunas
            tabela = Table(
                data,
                colWidths=[3.2 * cm, 5 * cm, 5 * cm, 4 * cm, 3 * cm],
                repeatRows=1  # repete cabeçalho se o relatório for grande
            )
            tabela.hAlign = 'CENTER'

            estilo_tabela = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.95, 0.72, 0.02)),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TOPPADDING', (0, 1), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                ('BOX', (0, 0), (-1, -1), 1.2, colors.gray),
                ('GRID', (0, 0), (-1, -1), 0.7, colors.gray),
            ])

            for i, pos in enumerate(fila, start=1):
                cor = colors.green if not pos.status else colors.red
                estilo_tabela.add('TEXTCOLOR', (-1, i), (-1, i), cor)

            tabela.setStyle(estilo_tabela)
            elements.append(Spacer(1, 0.7 * cm))
            elements.append(tabela)
            elements.append(Spacer(1, 1.0 * cm))


    # ========== RELATÓRIO DO GERADOR ==========
    else:
        doacoes = Donation.query.filter_by(id_gerador=gen.id).order_by(Donation.data_doacao.desc()).all()

        if not doacoes:
            elements.append(Paragraph("Nenhuma doação encontrada para este gerador.", normal_style))
        else:
            data = [["Data", "Quantidade Doada", "Quantidade Disponível", "Status"]]

            for d in doacoes:
                data_doacao = d.data_doacao.strftime("%d/%m/%Y") if d.data_doacao else "—"
                qtd_doada = d.quantidade_doacao or 0
                qtd_disp = d.quantidade_disponivel or 0
                status_text = "Concluído" if not d.status else "Pendente"
                data.append([f'{data_doacao}', f'{qtd_doada} KWh', f'{qtd_disp} KWh', status_text])

            tabela = Table(data, colWidths=[4 * cm, 5.5 * cm, 5.5 * cm, 4 * cm])

            estilo_tabela = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.95, 0.72, 0.02)),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TOPPADDING', (0, 1), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                ('BOX', (0, 0), (-1, -1), 1.2, colors.gray),
                ('GRID', (0, 0), (-1, -1), 0.7, colors.gray),
            ])

            for i, d in enumerate(doacoes, start=1):
                cor = colors.green if not d.status else colors.red
                estilo_tabela.add('TEXTCOLOR', (-1, i), (-1, i), cor)

            tabela.setStyle(estilo_tabela)
            elements.append(Spacer(1, 0.7 * cm))
            elements.append(tabela)
            elements.append(Spacer(1, 1.0 * cm))

    doc.build(elements)
    buffer.seek(0)

    nome = "beneficiario" if tipo_usuario == 1 else "gerador"
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"relatorio_{nome}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
        mimetype='application/pdf'
    )
