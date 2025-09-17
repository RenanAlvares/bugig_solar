from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from forms import FormBenef
from extensions import db
from models_DB import Beneficiarios, TipoClasses, UsersDb
import os

@auth_bp.route('/beneficiario/<int:user_id>', methods=['GET', 'POST'])
def cadastrar_beneficiario(user_id):
    form = FormBenef()
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

    return render_template('Beneficiario.html', form=form)
