from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from base import DBConnection  # Importando a classe de conexão com o banco de dados

# Criando o Blueprint para o login
login_bp = Blueprint('login', __name__, template_folder='templates')

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Processa o login de alunos."""
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        if not email or not senha:
            flash("Por favor, preencha todos os campos.", "warning")
            return render_template('login.html')

        # Conectar ao banco de dados através do DBConnection
        db = DBConnection()

        try:
            # Verifica se o email e senha pertencem a um aluno
            aluno = db.aluno_login(email, senha)

            if aluno:
                session.clear()
                session['usuario_id'] = aluno['id']  # ID do aluno
                session['usuario_nome'] = aluno['nome']  # Nome do aluno
                session['tipo'] = 'aluno'
                return redirect(url_for('aluno.home_aluno'))
            else:
                flash("Email ou senha incorretos.", "danger")

        except Exception as e:
            print(f"Erro ao processar login: {e}")
            flash("Erro interno. Tente novamente.", "danger")

    return render_template('login.html')
