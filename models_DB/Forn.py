from Main import db

class Forn(db.Model):
    
    __tablename__ = 'Fornecedores'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuarioF = db.Column(db.Integer, db.ForeignKey('Usuarios.id'), nullable=False)
    razao_social = db.Column(db.String(40), nullable=True)
    telefone_comercial = db.Column(db.String(20), nullable=False)
    # banco dos fornecedores