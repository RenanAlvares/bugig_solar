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

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        if self.tipo_documento.data == 'cnpj':
            if not self.nome_fantasia.data or self.nome_fantasia.data.strip() == '':
                self.nome_fantasia.errors.append('Nome Fantasia é obrigatório para CNPJ.')
                return False

        return True


    def __repr__(self):
        return f'<Usuario {self.nm_user}>'