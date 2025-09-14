from Main import app
from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from forms.form_donation import FormDonation
from models_DB.companies import DistribuidoraModel


@app.route('/donation', methods=['POST', 'GET'])
def donation():
    
    form = FormDonation()
    form.distribuidora.choices = [(d.id_distribuidora, d.nome_distribuidora) for d in DistribuidoraModel.query.all()]
    # seleciona todas as distribuidoras cadastradas no banco


    if form.validate_on_submit():
        qtd = form.qtd_doada.data
        distribuidora_id = form.distribuidora.data

        print(f'Sua doação de {qtd} unidades foi realizada com sucesso!')
        return url_for('bugig') # após doar retorna para a tela de menu principal
    return render_template('donation.html', form=form)