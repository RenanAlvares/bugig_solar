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
    from flask import abort, send_file
    import io
    import csv
    from datetime import datetime

    benef = Beneficiaries.query.filter_by(id_user=user_id).first()
    gen = Generators.query.filter_by(id_user=user_id).first()

    if benef:
        tipo_usuario = 1
    elif gen:
        tipo_usuario = 2
    else:
        abort(404)

    # Criar buffer de texto para o CSV
    output = io.StringIO()
    writer = csv.writer(output, delimiter=';', quoting=csv.QUOTE_MINIMAL)

    # Cabeçalho do relatório
    titulo = "Relatório do Beneficiário" if tipo_usuario == 1 else "Relatório do Gerador"
    writer.writerow([titulo])
    writer.writerow([f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M')}"])
    writer.writerow([])  # Linha em branco

    # ========== RELATÓRIO DO BENEFICIÁRIO ==========
    if tipo_usuario == 1:
        fila = Queue.query.filter_by(id_beneficiario=benef.id).order_by(Queue.data_solicitacao.desc()).all()

        if not fila:
            writer.writerow(["Nenhum registro encontrado na sua fila."])
        else:
            # Cabeçalho da tabela
            writer.writerow([
                "Data",
                "Quantidade Solicitada (KWh)",
                "Créditos Recebidos (KWh)",
                "Valor Economizado (R$)",
                "Status"
            ])

            # Dados
            for pos in fila:
                data_solic = pos.data_solicitacao.strftime("%d/%m/%Y") if pos.data_solicitacao else "—"
                qtd_solicitada = pos.quantidade_solicitada or 0
                qtd_recebida = pos.quantidade_recebida or 0
                valor = f"{qtd_recebida * 0.90:.2f}" if qtd_recebida else "—"
                status_text = "Concluído" if not pos.status else "Pendente"
                
                writer.writerow([
                    data_solic,
                    qtd_solicitada,
                    qtd_recebida,
                    valor,
                    status_text
                ])

    # ========== RELATÓRIO DO GERADOR ==========
    else:
        doacoes = Donation.query.filter_by(id_gerador=gen.id).order_by(Donation.data_doacao.desc()).all()

        if not doacoes:
            writer.writerow(["Nenhuma doação encontrada para este gerador."])
        else:
            # Cabeçalho da tabela
            writer.writerow([
                "Data",
                "Quantidade Doada (KWh)",
                "Quantidade Disponível (KWh)",
                "Status"
            ])

            # Dados
            for d in doacoes:
                data_doacao = d.data_doacao.strftime("%d/%m/%Y") if d.data_doacao else "—"
                qtd_doada = d.quantidade_doacao or 0
                qtd_disp = d.quantidade_disponivel or 0
                status_text = "Concluído" if not d.status else "Pendente"
                
                writer.writerow([
                    data_doacao,
                    qtd_doada,
                    qtd_disp,
                    status_text
                ])

    # Preparar o arquivo para download
    output.seek(0)
    
    # Converter StringIO para BytesIO com encoding UTF-8 + BOM (para Excel)
    csv_bytes = io.BytesIO()
    csv_bytes.write('\ufeff'.encode('utf-8'))  # BOM para UTF-8
    csv_bytes.write(output.getvalue().encode('utf-8'))
    csv_bytes.seek(0)

    nome = "beneficiario" if tipo_usuario == 1 else "gerador"
    return send_file(
        csv_bytes,
        as_attachment=True,
        download_name=f"relatorio_{nome}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mimetype='text/csv'
    )