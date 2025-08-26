from Main import db

class TipoModel(db.Model):

    __tablename__ = 'Tipos_usuarios'

    id_tipo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_tipo = db.Column(db.String(20), nullable=False)