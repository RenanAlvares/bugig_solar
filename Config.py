'''SECRET_KEY = 'teste123'

SQLALCHEMY_DATABASE_URI = '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
    SGBD = 'mysql+pymysql',
    usuario = 'root',
    senha = 'Renan123',
    servidor = 'localhost',
    database = 'projeto_interdisciplinar'
)

SQLALCHEMY_TRACK_MODIFICATIONS = False'''

'''SQLALCHEMY_DATABASE_URI = '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
    SGBD = 'mysql+pymysql',
    usuario = 'root',
    senha = '15072004',
    servidor = 'localhost',
    database = 'projeto_interdisciplinar'
)
SQLALCHEMY_TRACK_MODIFICATIONS = False'''

import os

SECRET_KEY = os.environ.get('SECRET_KEY', 'teste123')

# ==========================================
# BANCO DE DADOS
# ==========================================

# Em produção, usa PostgreSQL do Render
# Em desenvolvimento local, usa MySQL
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # PRODUÇÃO (Render)
    # Render usa postgres:// mas SQLAlchemy precisa de postgresql://
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    print("☁️  Usando PostgreSQL (Render)")
else:
    # DESENVOLVIMENTO LOCAL (MySQL)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Renan123@localhost/projeto_interdisciplinar'
    print("🔧 Usando MySQL (Local)")

SQLALCHEMY_TRACK_MODIFICATIONS = False

# Pool de conexões
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 5,
    'pool_recycle': 3600,
    'pool_pre_ping': True,
}