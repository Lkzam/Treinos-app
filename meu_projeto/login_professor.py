from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from base import DBConnection  # Importa a classe de conexão com o banco de dados

# Criando um Blueprint para login de professores
login_professor_bp = Blueprint('login_professor', __name__, template_folder='templates')

# Rota para login de professor
@login_professor_bp.route('/login_professor', methods=['GET', 'POST'])
def login_professor():
    """Realiza o login do professor"""

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        senha = request.form.get('senha', '').strip()

        if not email or not senha:
            flash("Preencha todos os campos!", "danger")
            return render_template('login_professor.html')

        db = DBConnection()

        try:
            # Verifica se o professor existe e se a senha está correta
            professor = db.professor_login(email, senha)

            if professor:
                print(f"✅ Login bem-sucedido: {professor}")  # Debug

                # Configura a sessão do professor
                session.clear()  # Limpa qualquer sessão anterior
                session['professor_id'] = professor['id']
                session['professor_nome'] = professor['nome']
                session['tipo'] = 'professor'
                session.permanent = True  # Mantém a sessão ativa

                flash(f"Bem-vindo, {professor['nome']}!", "success")
                return redirect(url_for('professor.home_professor'))  # Redireciona para home

            print("❌ Login falhou! Verifique email e senha.")  # Debug
            flash("Email ou senha inválidos!", "danger")

        except Exception as e:
            print(f"❌ Erro no login do professor: {e}")  # Log do erro
            flash("Erro interno no sistema. Tente novamente.", "danger")

    return render_template('login_professor.html')
