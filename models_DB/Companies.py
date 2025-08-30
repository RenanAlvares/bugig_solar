from Main import db

class DistribuidoraModel(db.Model):

    __tablename__ = 'Distribuidoras'

    id_distribuidora = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_distribuidora = db.Column(db.String(70), nullable=False)

    def __repr__(self):
        return f"<Distribuidora {self.nome_distribuidora}>"