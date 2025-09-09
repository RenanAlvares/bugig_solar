SECRET_KEY = 'teste123'

SQLALCHEMY_DATABASE_URI = '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
    SGBD = 'mysql+pymysql',
    usuario = 'root',
    senha = 'Renan123',
    servidor = 'localhost',
    database = 'projeto_interdisciplinar'
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
