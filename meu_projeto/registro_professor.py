from flask import Blueprint, request, render_template, redirect, url_for, flash
from base import DBConnection  # Importa a classe de conexão com o banco de dados

# Definindo o Blueprint para o registro de professor
registro_professor_bp = Blueprint('registro_professor', __name__, url_prefix="/registrar_professor")

# Rota para a tela de registro do professor
@registro_professor_bp.route('/', methods=['GET', 'POST'])
def registrar_professor():
    """Renderiza a página de registro do professor e trata o POST."""
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        especialidade = request.form['especialidade']

        if not nome or not email or not senha or not especialidade:
            flash("Todos os campos são obrigatórios!", "danger")
            return render_template('register_professor.html')

        # Conectar ao banco de dados e verificar se o e-mail já está cadastrado
        db = DBConnection()
        if db.aluno_existe(email):
            flash("Este e-mail já está cadastrado como aluno!", "danger")
            return render_template('register_professor.html')

        try:
            # Registrando o professor no banco de dados
            print(f"Tentando registrar professor: {nome}, {email}, {senha}, {especialidade}")
            db.professor_register(nome, email, senha, especialidade)
            flash("Cadastro realizado com sucesso!", "success")
            print(f"Professor {nome} registrado com sucesso!")
            return redirect(url_for('login.login'))  # Redirecionando para login
        except Exception as e:
            flash(f"Erro ao registrar professor: {e}", "danger")
            print(f"Erro ao registrar professor: {e}")

    return render_template('register_professor.html')
