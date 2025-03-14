from flask import Blueprint, render_template, session, redirect, url_for
from base import DBConnection  # Importando a classe DBConnection

aluno_bp = Blueprint('aluno', __name__, template_folder='templates')

@aluno_bp.route('/home_aluno')
def home_aluno():
    """Página inicial do aluno."""
    if 'usuario_id' not in session or session['tipo'] != 'aluno':
        return redirect(url_for('login.login'))  # Redireciona para o login se não estiver autenticado

    db = DBConnection()

    try:
        # Busque os treinos do aluno pelo seu ID
        treinos = db.fetchall("SELECT nome, descricao FROM treinos WHERE aluno_id = ?", [session['usuario_id']])

        return render_template('home_aluno.html', treinos=treinos)

    except Exception as e:
        print(f"Erro ao buscar treinos: {e}")
        return render_template('home_aluno.html', error="Erro ao carregar os treinos.")
