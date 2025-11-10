#!/usr/bin/env bash
set -o errexit

# Instala dependências
pip install -r requirements.txt

# Inicializa banco (só na primeira vez)
python init_db.py

# Dar permissão Linux / Mac
chmod +x build.sh