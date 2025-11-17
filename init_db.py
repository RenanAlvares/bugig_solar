"""
Script de Inicialização do Banco de Dados
==========================================
Popula o banco com dados iniciais (tipos, distribuidoras, etc.)
Roda automaticamente no primeiro deploy do Render.

USO:
    python init_db.py              # popula o banco
    python init_db.py --force      # força repopular
    python init_db.py --reset      # apaga tudo e recria
"""

import sys
import os
from main import app
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
            # 1. Tipos de Usuário (2)
            print("   → Tipos de usuário...")
            tipos_usuario = [
                TipoUser(id=1, nome_tipo_user='Beneficiário'),
                TipoUser(id=2, nome_tipo_user='Gerador')
            ]
            for tipo in tipos_usuario:
                db.session.merge(tipo)
            db.session.commit()
            print("   ✓ Tipos de usuário (2)")
            
            # 2. Tipos de Pessoa (2)
            print("   → Tipos de pessoa...")
            tipos_pessoa = [
                TipoPessoa(id=1, tipo_pessoa='Física'),
                TipoPessoa(id=2, tipo_pessoa='Jurídica')
            ]
            for tipo in tipos_pessoa:
                db.session.merge(tipo)
            db.session.commit()
            print("   ✓ Tipos de pessoa (2)")
            
            # 3. Tipos de Pagamento (4)
            print("   → Tipos de pagamento...")
            tipos_pagamento = [
                TipoPagamento(id=1, nome_tipo='Pix'),
                TipoPagamento(id=2, nome_tipo='Cartão de Crédito'),
                TipoPagamento(id=3, nome_tipo='Boleto Bancário'),
                TipoPagamento(id=4, nome_tipo='Pendente')
            ]
            for tipo in tipos_pagamento:
                db.session.merge(tipo)
            db.session.commit()
            print("   ✓ Tipos de pagamento (4)")
            
            # 4. Classes de Consumo (3)
            print("   → Classes de consumo...")
            classes_consumo = [
                TipoClasses(id=1, nome_tipo_classe='Residencial'),
                TipoClasses(id=2, nome_tipo_classe='Comercial'),
                TipoClasses(id=3, nome_tipo_classe='Industrial')
            ]
            for classe in classes_consumo:
                db.session.merge(classe)
            db.session.commit()
            print("   ✓ Classes de consumo (3)")
            
            # 5. Tipos de Geração (3)
            print("   → Tipos de geração...")
            tipos_geracao = [
                TipoGeracao(id=1, nome_tipo_geracao='Solar Fotovoltaica'),
                TipoGeracao(id=2, nome_tipo_geracao='Eólica'),
                TipoGeracao(id=3, nome_tipo_geracao='Biomassa')
            ]
            for tipo in tipos_geracao:
                db.session.merge(tipo)
            db.session.commit()
            print("   ✓ Tipos de geração (3)")
            
            # 6. Distribuidoras (3)
            print("   → Distribuidoras...")
            distribuidoras = [
                Companies(id=1, nome_distribuidora='Neoenergia'),
                Companies(id=2, nome_distribuidora='Enel'),
                Companies(id=3, nome_distribuidora='Cemig')
            ]
            for dist in distribuidoras:
                db.session.merge(dist)
            db.session.commit()
            print("   ✓ Distribuidoras (3)")
            
            print("\n✅ Banco populado com sucesso!")
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Erro ao popular dados: {e}")
            import traceback
            traceback.print_exc()
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
    print("   - 4 tipos de pagamento (Pix, Cartão, Boleto, Pendente)")
    print("   - 3 classes de consumo (Residencial, Comercial, Industrial)")
    print("   - 3 tipos de geração (Solar, Eólica, Biomassa)")
    print("   - 3 distribuidoras (Neoenergia, Enel, Cemig)")

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