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
    user_id = session.get('new_user_id')

    if not user_id:
        flash('Usuário não informado na sessão', 'danger')
        return redirect(url_for('auth.signin'))

    form_benef = FormBenef()
    # Pega as classes de consumo do banco
    classe_consumo = TipoClasses.query.all()
    form_benef.classe_consumo.choices = [(str(c.id), c.nome_tipo_classe) for c in classe_consumo]

    if form_benef.validate_on_submit():
        arquivos = [form_benef.conta1.data, form_benef.conta2.data, form_benef.conta3.data]
        consumos = []

        for arquivo in arquivos:
            arquivo.seek(0)
            conteudo = arquivo.read().decode("utf-8").strip().splitlines()
            linha2 = conteudo[1].strip()
            consumo = float(linha2.split()[1])
            consumos.append(consumo)

        consumo_mensal = int(sum(consumos) / len(consumos))
        classe_consumo_id = int(form_benef.classe_consumo.data)

        novo_beneficiario = Beneficiaries(
            consumo_mensal=consumo_mensal,
            classe_consumo=classe_consumo_id,
            id_user=user_id
        )

        try:
            db.session.add(novo_beneficiario)
            db.session.commit()
            flash('Beneficiário cadastrado com sucesso!', 'success')

            # Remove o ID da sessão após criar o beneficiário
            session.pop('new_user_id', None)
            return redirect(url_for('auth.menu_benef'))

        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao salvar beneficiário: {str(e)}", "danger")

    return render_template('benef.html', titulo=titulo, form_benef=form_benef)





@auth_bp.route('/new-gen', methods=['GET', 'POST'])
@login_required
def signin_gen():

    # Recupera o ID do usuário da sessão
    user_id = session.get('new_user_id')
    if not user_id:
        flash('Usuário não informado na sessão', 'danger')
        return redirect(url_for('auth.menu_benef'))

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
            id_user=user_id
        )

        db.session.add(novo_gerador)
        db.session.commit()
        flash('Gerador cadastrado com sucesso!', 'success')

        # Remove o ID da sessão após criar o gerador
        session.pop('new_user_id', None)

        return redirect(url_for('public.landing_page'))  # mudar para auth.menu_gen quando houver o template

    return render_template('Gerador.html', form=form_gen)

