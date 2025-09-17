from extensions import db

class TipoUser(db.Model):
    __tablename__ = 'tipo_usuario'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_tipo_user = db.Column(db.String(45), nullable=False)

    def __repr__(self):
        return f'<TipoUser {self.nome_tipo_user}>'


class TipoPagamento(db.Model):
    __tablename__ = 'tipo_pagamento'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_tipo = db.Column(db.String(45), nullable=False)

    def __repr__(self):
        return f'<TipoPagamento {self.nome_tipo}>'


class TipoClasses(db.Model):
    __tablename__ = 'Tipo_Classes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_tipo_classe = db.Column(db.String(45), nullable=False)

    def __repr__(self):
        return f'<TipoClasses {self.nome_tipo_classe}>'


class TipoGeracao(db.Model):
    __tablename__ = 'Tipo_geracao'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_tipo_geracao = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<TipoGeracao {self.nome_tipo_geracao}>'


class TipoPessoa(db.Model):
    __tablename__ = 'tipo_pessoa'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo_pessoa = db.Column(db.String(45), nullable=False)

    def __repr__(self):
        return f'<TipoPessoa {self.tipo_pessoa}>'
