from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
import importlib
import os

# Criar a aplicação Flask
app = Flask(__name__)

# 📌 Configuração do banco de dados (SQL Server)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "uma_chave_realmente_segura")  # Use uma chave fixa para evitar perda de sessão
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Dicionário com os Blueprints para importar dinamicamente
blueprints = {
    "login": "login_bp",
    "registro": "registro_bp",
    "professor": "professor_bp",
    "registro_professor": "registro_professor_bp",
    "login_professor": "login_professor_bp",
    "aluno": "aluno_bp"
}

# Inicializar os Blueprints dinamicamente
for nome_modulo, nome_bp in blueprints.items():
    try:
        modulo = importlib.import_module(nome_modulo)  # Importa dinamicamente
        blueprint = getattr(modulo, nome_bp, None)  # Obtém o Blueprint
        if blueprint:
            app.register_blueprint(blueprint)
            print(f"✅ [SUCESSO] Blueprint '{nome_bp}' registrado.")
        else:
            print(f"⚠️ [AVISO] Blueprint '{nome_bp}' não encontrado no módulo '{nome_modulo}'.")
    except ModuleNotFoundError as e:
        print(f"❌ [ERRO] Módulo '{nome_modulo}' não encontrado: {e}")
    except AttributeError as e:
        print(f"❌ [ERRO] Blueprint '{nome_bp}' não encontrado no módulo '{nome_modulo}': {e}")
    except Exception as e:
        print(f"❌ [ERRO] Falha ao carregar '{nome_modulo}': {e}")

# 📌 Rota principal para redirecionar para a página de login
@app.route('/', methods=['GET'])
def index():
    """Redireciona para a página de login."""
    return redirect(url_for('login.login'))

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)  # Apenas no seu PC
