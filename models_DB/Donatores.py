from Main import db

class Donatores(db.Model):

    __tablename__ = 'Doacao'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user_doacao = db.Column(db.Integer, db.ForeignKey('Usuarios.id'), nullable=False)
    quantidade_doacao = db.Column(db.Integer, nullable=False)
    distribuidora = db.Column(db.String(100), nullable=False)