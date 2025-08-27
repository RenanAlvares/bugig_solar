from Main import db
from flask_wtf import FlaskForm 

class UsersDb(db.Model):

    __tablename__ = 'Usuarios'
    # como está no banco de dados
    
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    id_tipo = db.Column(db.Integer, db.ForeignKey('Tipos_usuarios.id_tipo'), nullable=False)
    nome = db.Column(db.String(55), nullable = False)
    email = db.Column(db.String(60), nullable = False)
    documento = db.Column(db.String(15), nullable = False)
    cep = db.Column(db.String(15), nullable = False)
    numero = db.Column(db.Integer(5), nullable = False)
    senha = db.Column(db.String(10), nullable = False)
    telefone = db.Column(db.String(15), nullable = False)
    razao_social = db.Column(db.String(100), nullable = True)
    id_distribuidora = db.Column(db.Integer, db.ForeignKey('Distribuidoras.id_distribuidora'), nullable = False)


    def __repr__(self):
        return f'<Usuario {self.nome}>'