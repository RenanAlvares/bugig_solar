from flask import Flask
from extensions import db, csrf
import os
from controllers.public_routes import public_bp
from controllers.login import auth_bp
from controllers.errors import errors_bp

# Define o diretório base do projeto
basedir = os.path.abspath(os.path.dirname(__file__))

# Cria a aplicação Flask com caminhos explícitos
app = Flask(
    __name__,
    template_folder=os.path.join(basedir, 'templates'),
    static_folder=os.path.join(basedir, 'static')
)

app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'uploads', 'fotos_perfil')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

app.config.from_pyfile('Config.py')

db.init_app(app)
csrf.init_app(app)

# ====== DEBUG - VERIFICAR CAMINHOS NO RENDER ======
print("\n" + "="*60)
print("🔍 DEBUG - INFORMAÇÕES DE CAMINHOS")
print("="*60)
print(f"📁 Diretório base: {basedir}")
print(f"📁 Diretório atual (cwd): {os.getcwd()}")
print(f"📁 Template folder: {app.template_folder}")
print(f"📁 Static folder: {app.static_folder}")

# Verifica se a pasta templates existe
if os.path.exists(app.template_folder):
    print(f"✅ Pasta templates EXISTE em: {app.template_folder}")
    try:
        arquivos = os.listdir(app.template_folder)
        print(f"📄 Arquivos encontrados ({len(arquivos)}): {arquivos}")
    except Exception as e:
        print(f"❌ Erro ao listar arquivos: {e}")
else:
    print(f"❌ Pasta templates NÃO EXISTE em: {app.template_folder}")
    
    # Tenta encontrar onde está a pasta templates
    print("\n🔍 Procurando pasta 'templates' em locais comuns...")
    for caminho in [os.getcwd(), basedir, '/opt/render/project/src']:
        templates_path = os.path.join(caminho, 'templates')
        if os.path.exists(templates_path):
            print(f"✅ ENCONTRADA em: {templates_path}")
            print(f"   Arquivos: {os.listdir(templates_path)}")
        else:
            print(f"❌ NÃO encontrada em: {templates_path}")

print("="*60 + "\n")
# ====== FIM DEBUG ======

# registra blueprints
app.register_blueprint(public_bp)
app.register_blueprint(auth_bp, url_prefix='/bugig')
app.register_blueprint(errors_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5001)