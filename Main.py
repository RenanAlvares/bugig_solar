from flask import Flask
from extensions import db, csrf
import os
from controllers.public_routes import public_bp
from controllers.login import auth_bp  # importa blueprint já com todas as rotas
from controllers.errors import errors_bp

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads', 'fotos_perfil')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

app.config.from_pyfile('config.py')

db.init_app(app)
csrf.init_app(app)

# registra blueprints
app.register_blueprint(public_bp)
app.register_blueprint(auth_bp, url_prefix='/bugig')
app.register_blueprint(errors_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5001)

# estou fazendo alguns ajustes aqui ainda
"""
Script de Inicialização do Banco de Dados
==========================================
Popula o banco com dados iniciais (tipos, distribuidoras, etc.)
Roda automaticamente no primeiro deploy do Render.

USO:
    python init_db.py              # popula o banco configurado
    python init_db.py --reset      # apaga e recria tudo (CUIDADO!)
"""

import sys
import os
from Main import app
from extensions import db
from models_DB.users import UsersDb
from models_DB.companies import Companies
from models_DB.types import TipoUser, TipoPagamento, TipoClasses, TipoGeracao, TipoPessoa
from models_DB.benef_gen import Beneficiaries, Generators
from models_DB.donation_queue import Donation, Queue
from models_DB.transfer import Transfer
from models_DB.payments import Payment

def verificar_banco_ja_populado():
    """Verifica se o banco já tem dados iniciais"""
    with app.app_context():
        try:
            # Se já tem tipos de usuário, o banco já foi populado
            if TipoUser.query.first() is not None:
                return True
            return False
        except Exception as e:
            # Tabelas não existem ainda
            return False

def criar_tabelas():
    """Cria todas as tabelas do banco"""
    with app.app_context():
        print("🏗️  Criando estrutura das tabelas...")
        try:
            db.create_all()
            print("✅ Tabelas criadas com sucesso!")
            return True
        except Exception as e:
            print(f"❌ Erro ao criar tabelas: {e}")
            return False

def popular_dados():
    """Popula o banco com dados iniciais obrigatórios"""
    with app.app_context():
        print("📝 Populando dados iniciais...")
        
        try:
            # 1. Tipos de Usuário
            print("   → Tipos de usuário...")
            tipos_usuario = [
                TipoUser(id=1, nome_tipo_user='Beneficiário'),
                TipoUser(id=2, nome_tipo_user='Gerador')
            ]
            for tipo in tipos_usuario:
                db.session.merge(tipo)  # merge evita duplicação
            db.session.commit()
            print("   ✓ Tipos de usuário")
            
            # 2. Tipos de Pessoa
            print("   → Tipos de pessoa...")
            tipos_pessoa = [
                TipoPessoa(id=1, tipo_pessoa='Pessoa Física'),
                TipoPessoa(id=2, tipo_pessoa='Pessoa Jurídica')
            ]
            for tipo in tipos_pessoa:
                db.session.merge(tipo)
            db.session.commit()
            print("   ✓ Tipos de pessoa")
            
            # 3. Tipos de Pagamento
            print("   → Tipos de pagamento...")
            tipos_pagamento = [
                TipoPagamento(id=1, nome_tipo='PIX'),
                TipoPagamento(id=2, nome_tipo='Cartão de Crédito'),
                TipoPagamento(id=3, nome_tipo='Boleto'),
                TipoPagamento(id=4, nome_tipo='Pendente')
            ]
            for tipo in tipos_pagamento:
                db.session.merge(tipo)
            db.session.commit()
            print("   ✓ Tipos de pagamento")
            
            # 4. Classes de Consumo
            print("   → Classes de consumo...")
            classes_consumo = [
                TipoClasses(id=1, nome_tipo_classe='Residencial'),
                TipoClasses(id=2, nome_tipo_classe='Industrial'),
                TipoClasses(id=3, nome_tipo_classe='Comercial'),
                TipoClasses(id=4, nome_tipo_classe='Rural'),
                TipoClasses(id=5, nome_tipo_classe='Poder Público')
            ]
            for classe in classes_consumo:
                db.session.merge(classe)
            db.session.commit()
            print("   ✓ Classes de consumo")
            
            # 5. Tipos de Geração
            print("   → Tipos de geração...")
            tipos_geracao = [
                TipoGeracao(id=1, nome_tipo_geracao='Solar Fotovoltaica'),
                TipoGeracao(id=2, nome_tipo_geracao='Eólica'),
                TipoGeracao(id=3, nome_tipo_geracao='Hídrica (PCH)'),
                TipoGeracao(id=4, nome_tipo_geracao='Biomassa'),
                TipoGeracao(id=5, nome_tipo_geracao='Biogás')
            ]
            for tipo in tipos_geracao:
                db.session.merge(tipo)
            db.session.commit()
            print("   ✓ Tipos de geração")
            
            # 6. Distribuidoras (principais do Brasil)
            print("   → Distribuidoras...")
            distribuidoras = [
                Companies(id=1, nome_distribuidora='CPFL Paulista'),
                Companies(id=2, nome_distribuidora='Enel SP'),
                Companies(id=3, nome_distribuidora='Enel RJ'),
                Companies(id=4, nome_distribuidora='Light'),
                Companies(id=5, nome_distribuidora='Cemig'),
                Companies(id=6, nome_distribuidora='Copel'),
                Companies(id=7, nome_distribuidora='Celesc'),
                Companies(id=8, nome_distribuidora='CPFL Piratininga'),
                Companies(id=9, nome_distribuidora='EDP São Paulo'),
                Companies(id=10, nome_distribuidora='Energisa'),
                Companies(id=11, nome_distribuidora='Equatorial'),
                Companies(id=12, nome_distribuidora='Neoenergia Coelba'),
                Companies(id=13, nome_distribuidora='Neoenergia Cosern'),
                Companies(id=14, nome_distribuidora='RGE Sul'),
            ]
            for dist in distribuidoras:
                db.session.merge(dist)
            db.session.commit()
            print("   ✓ Distribuidoras")
            
            print("\n✅ Banco populado com sucesso!")
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Erro ao popular dados: {e}")
            return False

def resetar_banco():
    """Apaga e recria todo o banco (CUIDADO!)"""
    with app.app_context():
        print("\n⚠️  ATENÇÃO: Isso vai APAGAR todos os dados!")
        print("⚠️  Isso inclui: usuários, doações, transferências, etc.")
        resposta = input("⚠️  Digite 'SIM' para confirmar: ")
        
        if resposta.upper() != 'SIM':
            print("❌ Operação cancelada")
            return False
        
        print("🗑️  Removendo tabelas antigas...")
        try:
            db.drop_all()
            print("✅ Tabelas removidas!")
            return True
        except Exception as e:
            print(f"❌ Erro ao remover tabelas: {e}")
            return False

def main():
    """Função principal"""
    print("=" * 60)
    print("🚀 INICIALIZADOR DO BANCO DE DADOS")
    print("=" * 60)
    
    # Verifica argumentos
    reset = '--reset' in sys.argv
    force = '--force' in sys.argv
    
    # Verifica se já foi populado
    if verificar_banco_ja_populado() and not reset and not force:
        print("\n✅ Banco já está inicializado!")
        print("💡 Para repopular, use: python init_db.py --force")
        print("⚠️  Para resetar tudo, use: python init_db.py --reset")
        return
    
    # Reset se solicitado
    if reset:
        if not resetar_banco():
            return
    
    # Cria tabelas se não existirem
    if not criar_tabelas():
        return
    
    # Popula dados
    if not popular_dados():
        return
    
    print("\n" + "=" * 60)
    print("🎉 CONFIGURAÇÃO CONCLUÍDA!")
    print("=" * 60)
    print("\n💡 Próximos passos:")
    print("   1. Execute: python Main.py")
    print("   2. Acesse: http://localhost:5001")
    print("   3. Teste o cadastro e login!")
    print("\n📊 Dados populados:")
    print("   - 2 tipos de usuário (Beneficiário, Gerador)")
    print("   - 2 tipos de pessoa (Física, Jurídica)")
    print("   - 4 tipos de pagamento")
    print("   - 5 classes de consumo")
    print("   - 5 tipos de geração")
    print("   - 14 distribuidoras")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Operação cancelada pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Erro fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
