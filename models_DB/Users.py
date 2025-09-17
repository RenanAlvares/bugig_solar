from extensions import db
from flask_wtf import FlaskForm
from models_DB.types import TipoUser
from models_DB.companies import Companies
from models_DB.types import TipoPessoa  # precisa existir esse model também

class UsersDb(db.Model):
    __tablename__ = 'Usuarios'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column('Nome', db.String(45), nullable=False)
    email = db.Column('Email', db.String(45), nullable=False, unique=True)
    documento = db.Column('Documento', db.String(14), nullable=False)
    cep = db.Column('CEP', db.String(11), nullable=False)
    numero = db.Column('Numero', db.Integer, nullable=False)
    senha = db.Column('Senha', db.String(250), nullable=False)
    telefone = db.Column('Telefone', db.String(20), nullable=False)
    razao_social = db.Column('Razao_social', db.String(100), nullable=True)

    # FKs conforme banco
    id_tipo_user = db.Column(db.Integer, db.ForeignKey('tipo_usuario.id'), nullable=False)
    id_distribuidora = db.Column(db.Integer, db.ForeignKey('distribuidoras.id'), nullable=False)
    id_tipo_pessoa = db.Column(db.Integer, db.ForeignKey('tipo_pessoa.id'), nullable=False)

    # Relações
    tipo_usuario = db.relationship('TipoUser', backref='usuarios', lazy=True)
    distribuidora = db.relationship('Companies', backref='usuarios', lazy=True)
    tipo_pessoa = db.relationship('TipoPessoa', backref='usuarios', lazy=True)

    def __repr__(self):
        return f'<Usuario {self.nome}>'
