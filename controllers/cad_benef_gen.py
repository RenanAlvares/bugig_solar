from flask import render_template, redirect, url_for, flash
from controllers.login import user_owns_resource
from forms.form_benef import FormBenef
from forms.form_gen import FormGen
from extensions import db
from models_DB.benef_gen import Beneficiaries, Generators
from models_DB.types import TipoClasses, TipoGeracao
from . import auth_bp


@auth_bp.route('/<int:user_id>/new-benef', methods=['GET', 'POST'])
@user_owns_resource('user_id', tipo_usuario_esperado=1)
def signin_benef(user_id):
    titulo = 'Cadastro Beneficiário'

    form_benef = FormBenef()
    # Pega as classes de consumo do banco
    classe_consumo = TipoClasses.query.all()
    form_benef.classe_consumo.choices = [(str(c.id), c.nome_tipo_classe) for c in classe_consumo]

    if form_benef.validate_on_submit():
        arquivos = [form_benef.conta1.data, form_benef.conta2.data, form_benef.conta3.data]
        consumos = []

        try:
            for arquivo in arquivos:
                arquivo.seek(0)
                conteudo = arquivo.read().decode("utf-8").strip().splitlines()
                linha2 = conteudo[1].strip()
                consumo = float(linha2.split()[1])
                consumos.append(consumo)
        except Exception as e:
            flash(f"Erro ao processar os arquivos: {str(e)}", "danger")
            return render_template('benef.html', titulo=titulo, form_benef=form_benef)

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
            return redirect(url_for('auth.menu_benef', user_id=user_id))

        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao salvar beneficiário: {str(e)}", "danger")

    return render_template('benef.html', titulo=titulo, form_benef=form_benef)


@auth_bp.route('/<int:user_id>/new-gen', methods=['GET', 'POST'])
@user_owns_resource('user_id', tipo_usuario_esperado=2)
def signin_gen(user_id):
    form_gen = FormGen()
    titulo = 'Cadastro Gerador'

    # Pega os tipos de geração do banco
    tipos_geracao = TipoGeracao.query.all()
    form_gen.id_tipo_geracao.choices = [(str(g.id), g.nome_tipo_geracao) for g in tipos_geracao]

    if form_gen.validate_on_submit():  # Gerador
        producao_mensal = form_gen.producao_mensal.data
        inicio_operacao = form_gen.inicio_operacao.data  # DateField do WTForms já retorna date
        tipo_geracao_id = int(form_gen.id_tipo_geracao.data)

        novo_gerador = Generators(
            id_user=user_id,
            producao_mensal_med=producao_mensal,
            inicio_operacao=inicio_operacao,
            id_tipo_geracao=tipo_geracao_id
        )

        try:
            db.session.add(novo_gerador)
            db.session.commit()
            flash('Gerador cadastrado com sucesso!', 'success')
            return redirect(url_for('auth.menu_gen', user_id=user_id))

        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao salvar gerador: {str(e)}", "danger")

    return render_template('gen.html', titulo=titulo, form_gen=form_gen)
