from Main import db

class Estados(db.Model):
    
    __tablename__ = 'Estados'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(25), nullable=False)
    valor = db.Column(db.Float(3,2), nullable=False)
    taxa = db.Column(db.Integer(2), nullable=False)
