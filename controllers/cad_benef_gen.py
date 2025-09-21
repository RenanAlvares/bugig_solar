from flask import render_template, request, redirect, url_for, flash, session
from controllers.login import login_required
from forms.form_benef import FormBenef
from forms.form_gen import FormGen
from extensions import db
from models_DB.benef_gen import Beneficiaries, Generators
from models_DB.types import TipoClasses, TipoGeracao
from controllers.login import auth_bp


@auth_bp.route('/new-benef', methods=['GET', 'POST'])
@login_required
def signin_benef():

    titulo = 'Cadastro Beneficiário'
    # Recupera o ID do usuário da sessão
    user_id = session.get('new_user_id')
    if not user_id:
        flash('Usuário não informado na sessão', 'danger')
        return redirect(url_for('auth.signin'))

    form_benef = FormBenef()
    # Pega as classes de consumo do banco
    classe_consumo = TipoClasses.query.all()
    form_benef.classe_consumo.choices = [(str(c.id), c.nome_tipo_classe) for c in classe_consumo]

    if form_benef.validate_on_submit():  # Beneficiário
        arquivos = [form_benef.conta1.data, form_benef.conta2.data, form_benef.conta3.data]
        consumos = []

        try:
            for arquivo in arquivos:
                if not arquivo:
                    flash("Todos os arquivos devem ser enviados.", "danger")
                    return render_template("benef.html", titulo=titulo, form_benef=form_benef)

                arquivo.seek(0)  # garante que o ponteiro esteja no início
                conteudo = arquivo.read().decode("utf-8").strip().splitlines()

                if len(conteudo) < 2:
                    flash("Arquivo inválido. Deve conter nome na 1ª linha e data/valor na 2ª.", "danger")
                    return render_template("benef.html", titulo=titulo, form_benef=form_benef)

                linha2 = conteudo[1].strip()
                partes = linha2.split()

                if len(partes) != 2:
                    flash("Formato da 2ª linha inválido. Esperado: 'DATA VALOR'.", "danger")
                    return render_template("benef.html", titulo=titulo, form_benef=form_benef)

                consumo = float(partes[1])
                consumos.append(consumo)

            # média em inteiro
            consumo_mensal = int(sum(consumos) / len(consumos))
            classe_consumo_id = form_benef.classe_consumo.data

            # Cria o beneficiário vinculado ao usuário logado
            novo_beneficiario = Beneficiaries(
                consumo_mensal=consumo_mensal,
                classe_consumo=classe_consumo_id,
                id_usuario=user_id
            )

            db.session.add(novo_beneficiario)
            db.session.commit()
            flash(f'Beneficiário cadastrado com sucesso!', 'success')

            # Remove o ID da sessão após criar o beneficiário
            session.pop('new_user_id', None)

            return redirect(url_for('public.landing_page'))

        except Exception as e:
            flash(f"Erro ao processar arquivos: {str(e)}", "danger")

    # Renderiza o template caso GET ou falha na validação
    return render_template('benef.html', titulo=titulo, form_benef=form_benef)



@auth_bp.route('/new-gen', methods=['GET', 'POST'])
@login_required
def signin_gen():

    # Recupera o ID do usuário da sessão
    user_id = session.get('new_user_id')
    if not user_id:
        flash('Usuário não informado na sessão', 'danger')
        return redirect(url_for('auth.signin'))

    form_gen = FormGen()
    # Pega os tipos de geração do banco
    tipos_geracao = TipoGeracao.query.all()
    form_gen.id_tipo_geracao.choices = [(str(g.id), g.nome_tipo_geracao) for g in tipos_geracao]

    if form_gen.validate_on_submit():  # Gerador
        producao_mensal = form_gen.producao_mensal.data
        inicio_operacao = form_gen.inicio_operacao.data  # DateField do WTForms já retorna date
        tipo_geracao_id = form_gen.id_tipo_geracao.data

        # Cria o gerador vinculado ao usuário logado
        novo_gerador = Generators(
            producao_mensal=producao_mensal,
            inicio_operacao=inicio_operacao,
            id_tipo_geracao=tipo_geracao_id,
            id_usuario=user_id
        )

        db.session.add(novo_gerador)
        db.session.commit()
        flash('Gerador cadastrado com sucesso!', 'success')

        # Remove o ID da sessão após criar o gerador
        session.pop('new_user_id', None)

        return redirect(url_for('public.landing_page'))  # mudar para auth.menu_gen quando houver o template

    return render_template('Gerador.html', form=form_gen)



'''form = FormBenef()
# Puxando classes de consumo do banco
classes = TipoClasses.query.all()
form.classe_consumo.choices = [(str(c.id), c.nome_tipo_classe) for c in classes]

if form.validate_on_submit():
    arquivos = form.arquivos.data  # Lista de FileStorage
    consumos = []

    for arquivo in arquivos:
        filename = secure_filename(arquivo.filename)
        conteudo = arquivo.read().decode('utf-8')  # Lê como string
        try:
            valor = int(conteudo.strip())  # Considerando que o txt tem apenas um número
            consumos.append(valor)
        except ValueError:
            flash(f"Arquivo {filename} contém valor inválido.", "danger")
            return render_template('Beneficiario.html', form=form)

    if len(consumos) != 3:
        flash("Você deve enviar exatamente 3 arquivos.", "danger")
        return render_template('Beneficiario.html', form=form)

    media_consumo = int(sum(consumos) / 3)

    novo_benef = Beneficiarios(
        id_user=user_id,
        consumo_mensal=media_consumo,
        classe_consumo=int(form.classe_consumo.data)
    )

    db.session.add(novo_benef)
    db.session.commit()
    flash("Beneficiário cadastrado com sucesso!", "success")
    return redirect(url_for('public.landing_page'))

return render_template('Beneficiario.html', form=form)'''
