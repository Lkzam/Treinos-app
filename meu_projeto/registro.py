from flask import Blueprint, request, render_template, redirect, url_for, flash
from base import DBConnection  # Importa a classe de conexão com o banco de dados

# Definindo o Blueprint para o registro
registro_bp = Blueprint('registro', __name__, url_prefix="/registro")

# Rota para a tela de registro do aluno
@registro_bp.route('/', methods=['GET', 'POST'])
def registrar():
    """Renderiza a página de registro do aluno e trata o POST."""
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        if not nome or not email or not senha:
            flash("Todos os campos são obrigatórios!", "danger")
            return render_template('register.html')

        # Conectar ao banco de dados e verificar se o e-mail já está cadastrado
        db = DBConnection()
        if db.aluno_existe(email):
            flash("Este e-mail já está cadastrado!", "danger")
            return render_template('register.html')

        # Criando um novo aluno e salvando no banco (sem criptografia)
        db.aluno_register(nome, email, senha)

        flash("Cadastro realizado com sucesso!", "success")
        return redirect(url_for('login.login'))  # Redirecionando para login

    return render_template('register.html')
