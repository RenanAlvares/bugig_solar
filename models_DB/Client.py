from Main import db

class ClientDb(db.Model):

    __tablename__ = 'Clientes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuarios = db.Column(db.Integer, db.ForeignKey('Usuarios.id'), nullable=False)
    telefone_pessoal = db.Column(db.String(20), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)

