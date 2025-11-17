#!/usr/bin/env bash
# Script de build para o Render
set -o errexit

echo "📦 Instalando dependências..."
pip install -r requirements.txt

echo "🗄️  Inicializando banco de dados..."
python init_db.py

echo "✅ Build concluído!"