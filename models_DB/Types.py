from Main import db

class TipoModel(db.Model):

    __tablename__ = 'Tipos_usuarios'

    id_tipo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_tipo_user = db.Column(db.String(20), nullable=False)


class TipoPagamento(db.Model):

    __tablename__ = 'Tipo_pagamento'

    id = db.Column(db.Integer, primary_key=True)
    nome_tipo_pag = db.Column(db.String(100), nullable=False)


class TipoClasses(db.Model):

    __tablename__ = 'Tipo_Classes'

    id = db.Column(db.Integer, primary_key=True)
    nome_tipo_classe = db.Column(db.String(100), nullable=False)


class TipoGeracao(db.Model):

    __tablename__ = 'Tipo_Geracao'

    id = db.Column(db.Integer, primary_key=True)
    nome_tipo_geracao = db.Column(db.String(100), nullable=False)