from extensions import db

class Companies(db.Model):
    __tablename__ = 'distribuidoras'  # tudo minúsculo igual ao banco final

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_distribuidora = db.Column(db.String(70), nullable=False)

    def __repr__(self):
        return f"<Distribuidora {self.nome_distribuidora}>"
