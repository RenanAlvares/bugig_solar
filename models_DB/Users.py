from Main import db
from flask_wtf import FlaskForm 
from models_DB.types import TipoUser
from models_DB.companies import Companies

class UsersDb(db.Model):

    __tablename__ = 'Usuarios'
    # como está no banco de dados
    
    id_tipo = db.Column(db.Integer, db.ForeignKey('Tipos_usuarios.id_tipo'), nullable=False)
    id_distribuidora = db.Column(db.Integer, db.ForeignKey('Distribuidoras.id'), nullable = False)
    id_tipo_pessoa = db.Column(db.Integer, db.ForeignKey('Tipo_Pessoa.id'), nullable = False) 

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nome = db.Column(db.String(55), nullable = False)
    email = db.Column(db.String(60), nullable = False)
    documento = db.Column(db.String(15), nullable = False)
    cep = db.Column(db.String(15), nullable = False)
    numero = db.Column(db.Integer, nullable = False)
    senha = db.Column(db.String(200), nullable = False)
    telefone = db.Column(db.String(15), nullable = False)
    razao_social = db.Column(db.String(100), nullable = True)

    tipo_usuario = db.relationship('TipoUser', backref='usuarios', lazy=True)
    distribuidora = db.relationship('Companies', backref='usuarios', lazy=True)
    tipo_pessoa = db.relationship('TipoPessoa', backref='usuarios', lazy=True)


    def __repr__(self):
        return f'<Usuario {self.nome}>'