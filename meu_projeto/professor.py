from flask import Blueprint, render_template, session, redirect, url_for, flash, request, Flask

app = Flask(__name__)
from base import DBConnection  # Importa a classe de conexão com o banco de dados

professor_bp = Blueprint('professor', __name__, template_folder='templates')

# Rota para a página inicial do professor (home_professor)
@professor_bp.route('/home', methods=['GET'])
def home_professor():
    """Tela inicial do professor após login."""
    if 'professor_id' not in session:
        flash("Você precisa estar logado!", "warning")
        return redirect(url_for('login_professor.login_professor'))

    db = DBConnection()
    try:
        # Buscar apenas alunos que estão associados ao professor
        query = 'SELECT id, nome, email FROM alunos WHERE id IN (SELECT aluno_id FROM alunos_professores WHERE professor_id = ?)'
        alunos = db.fetchall(query, [session["professor_id"]])
        total_alunos = len(alunos)
        total_treinos = db.count('treinos')
        print(f"Total de alunos: {total_alunos}, Total de treinos: {total_treinos}")  # Log para depuração
    except Exception as e:
        flash(f"Erro ao carregar informações: {e}", "danger")
        total_alunos = total_treinos = 0
        alunos = []
        print(f"Erro ao carregar informações: {e}")  # Log de erro

    return render_template('home_professor.html', 
                           total_alunos=total_alunos,
                           total_treinos=total_treinos, 
                           alunos=alunos)

# Rota para acessar os treinos de um aluno ao clicar no nome
@professor_bp.route('/aluno/<int:aluno_id>/treinos', methods=['GET'])
def treinos_aluno(aluno_id):
    """Exibe os treinos de um aluno específico.""" 
    if 'professor_id' not in session:
        flash("Você precisa estar logado!", "warning")
        return redirect(url_for('login_professor.login_professor'))

    db = DBConnection()
    try:
        aluno = db.fetchone("SELECT nome FROM alunos WHERE id = ?", [aluno_id])
        if aluno is None:
            flash("Aluno não encontrado!", "danger")
            return redirect(url_for('professor.home_professor'))

        treinos = db.buscar_treinos_aluno(aluno_id)
        print(f"Treinos do aluno {aluno_id}: {treinos}")  # Log para depuração
    except Exception as e:
        flash(f"Erro ao carregar treinos do aluno: {e}", "danger")
        treinos = []
        print(f"Erro ao carregar treinos do aluno: {e}")  # Log de erro

    return render_template('treinos_aluno.html', aluno_nome=aluno[0], treinos=treinos, aluno_id=aluno_id)

# Rota para desassociar um aluno
@professor_bp.route('/desassociar_aluno/<int:aluno_id>', methods=['POST'])
def desassociar_aluno(aluno_id):
    """Desassocia um aluno do professor.""" 
    if 'professor_id' not in session:
        flash("Você precisa estar logado!", "warning")
        return redirect(url_for('login_professor.login_professor'))

    db = DBConnection()
    try:
        # Verifica se o aluno está associado ao professor
        aluno_assoc = db.get_one('alunos_professores', 'aluno_id', 'professor_id = ? AND aluno_id = ?', [session["professor_id"], aluno_id])
        if aluno_assoc:
            db.execute_query("DELETE FROM alunos_professores WHERE aluno_id = ? AND professor_id = ?", [aluno_id, session['professor_id']])
            flash("Aluno desassociado com sucesso!", "success")
            print(f"Aluno {aluno_id} desassociado com sucesso!")  # Log de sucesso
        else:
            flash("Esse aluno não está associado a você.", "warning")
            print(f"Aluno {aluno_id} não está associado ao professor {session['professor_id']}")  # Log de aviso
    except Exception as e:
        flash(f"Erro ao desassociar aluno: {e}", "danger")
        print(f"Erro ao desassociar aluno: {e}")  # Log de erro

    return redirect(url_for('professor.home_professor'))

# Rota para criar ou editar um treino
@professor_bp.route('/criar_treino', methods=['GET', 'POST'])
def criar_treino():
    """Cria um novo treino para um aluno específico.""" 
    if 'professor_id' not in session:
        flash("Você precisa estar logado!", "warning")
        return redirect(url_for('login_professor.login_professor'))

    if request.method == 'POST':
        treino_nome = request.form.get('nome_treino', '').strip()
        treino_descricao = request.form.get('descricao_treino', '').strip()
        aluno_id = request.form.get('aluno_id', '').strip()

        if not treino_nome or not treino_descricao or not aluno_id:
            flash("Por favor, preencha todos os campos do treino!", "danger")
            return redirect(url_for('professor.criar_treino', aluno_id=aluno_id))

        try:
            aluno_id = int(aluno_id)
            db = DBConnection()
            if db.get_one('alunos', 'id', 'id = ?', [aluno_id]):
                db.criar_treino(treino_nome, treino_descricao, aluno_id)
                flash("Treino criado com sucesso!", "success")
                print(f"Treino criado com sucesso para o aluno {aluno_id}")  # Log de sucesso
                return redirect(url_for('professor.treinos_aluno', aluno_id=aluno_id))
            else:
                flash("Aluno não encontrado!", "danger")
                print(f"Aluno {aluno_id} não encontrado")  # Log de erro
        except ValueError:
            flash("ID do aluno inválido!", "danger")
            print("ID do aluno inválido!")  # Log de erro
        except Exception as e:
            flash(f"Erro ao criar treino: {e}", "danger")
            print(f"Erro ao criar treino: {e}")  # Log de erro

        return redirect(url_for('professor.criar_treino', aluno_id=aluno_id))

    # Se o método for GET, renderiza o template de criação de treino
    aluno_id = request.args.get('aluno_id', '').strip()
    if not aluno_id:
        flash("ID do aluno não fornecido!", "danger")
        return redirect(url_for('professor.home_professor'))

    return render_template('criar_treino.html', aluno_id=aluno_id)

# Rota para editar um treino
@professor_bp.route('/editar_treino/<int:treino_id>', methods=['GET', 'POST'])
def editar_treino(treino_id):
    """Edita um treino existente.""" 
    if 'professor_id' not in session:
        flash("Você precisa estar logado!", "warning")
        return redirect(url_for('login_professor.login_professor'))

    db = DBConnection()
    if request.method == 'POST':
        treino_nome = request.form.get('nome_treino', '').strip()
        treino_descricao = request.form.get('descricao_treino', '').strip()
        aluno_id = request.form.get('aluno_id', '').strip()

        print(f"Recebido: Nome={treino_nome}, Descrição={treino_descricao}, Aluno ID={aluno_id}")  # DEBUG

        if not treino_nome or not treino_descricao or not aluno_id:
            flash("Por favor, preencha todos os campos do treino!", "danger")
            return redirect(url_for('professor.editar_treino', treino_id=treino_id))

        try:
            aluno_id = int(aluno_id)
            db.editar_treino(treino_id, treino_nome, treino_descricao)
            flash("Treino editado com sucesso!", "success")
            print("Treino atualizado com sucesso!")  # DEBUG
            return redirect(url_for('professor.treinos_aluno', aluno_id=aluno_id))
        except ValueError:
            flash("ID do aluno inválido!", "danger")
            print("ID do aluno inválido!")  # Log de erro
        except Exception as e:
            flash(f"Erro ao editar treino: {e}", "danger")
            print(f"Erro ao editar treino: {e}")  # DEBUG

    try:
        treino = db.get_one('treinos', 'id, nome, descricao, aluno_id', 'id = ?', [treino_id])
        if not treino:
            flash("Treino não encontrado!", "danger")
            return redirect(url_for('professor.home_professor'))
    except Exception as e:
        flash(f"Erro ao carregar treino: {e}", "danger")
        return redirect(url_for('professor.home_professor'))

    return render_template('editar_treino.html', treino=treino, aluno_id=treino[3])

# Rota para excluir um treino
@professor_bp.route('/excluir_treino/<int:treino_id>/<int:aluno_id>', methods=['GET', 'POST'])
def excluir_treino(treino_id, aluno_id):
    """Exclui um treino existente.""" 
    if 'professor_id' not in session:
        flash("Você precisa estar logado!", "warning")
        return redirect(url_for('login_professor.login_professor'))

    db = DBConnection()
    try:
        if request.method == 'POST':
            db.excluir_treino(treino_id)
            flash("Treino excluído com sucesso!", "success")
            return redirect(url_for('professor.treinos_aluno', aluno_id=aluno_id))

        treino = db.get_one('treinos', 'id, nome, descricao', 'id = ?', [treino_id])
        if not treino:
            flash("Treino não encontrado!", "danger")
            return redirect(url_for('professor.treinos_aluno', aluno_id=aluno_id))
    except Exception as e:
        flash(f"Erro ao excluir treino: {e}", "danger")
        return redirect(url_for('professor.treinos_aluno', aluno_id=aluno_id))

    return render_template('confirmar_exclusao.html', treino=treino, aluno_id=aluno_id)

# Rota para adicionar um aluno
@professor_bp.route('/adicionar_aluno', methods=['GET', 'POST'])
def adicionar_aluno():
    """Adiciona um novo aluno ao professor."""
    if 'professor_id' not in session:
        flash("Você precisa estar logado!", "warning")
        return redirect(url_for('login_professor.login_professor'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()

        if not email:
            flash("Por favor, preencha todos os campos!", "danger")
            return render_template('adicionar_aluno.html')

        db = DBConnection()
        try:
            # Verifica se o aluno já existe
            aluno = db.get_one('alunos', 'id, nome', 'email = ?', [email])
            if aluno:
                aluno_id = aluno[0]
                aluno_nome = aluno[1]
                print(f"Aluno encontrado: ID={aluno_id}, Nome={aluno_nome}")  # Log para verificar o aluno encontrado

                # Verifica se o aluno já está associado ao professor
                existing_assoc = db.get_one('alunos_professores', 'aluno_id', 'professor_id = ? AND aluno_id = ?', [session["professor_id"], aluno_id])
                if existing_assoc:
                    flash(f'O aluno {aluno_nome} já está associado a você!', 'warning')
                else:
                    # Associa o aluno ao professor
                    if db.associar_aluno_professor(aluno_id, session['professor_id']):
                        flash(f'Aluno {aluno_nome} associado com sucesso!', "success")
                    else:
                        flash(f"Erro ao associar aluno {aluno_nome} ao professor.", "danger")
            else:
                flash("Aluno não encontrado com esse email!", "danger")

        except Exception as e:
            print(f"Erro ao adicionar aluno: {e}")  # Log de erro
            flash(f"Erro ao adicionar aluno: {e}", "danger")

        return redirect(url_for('professor.adicionar_aluno'))

    return render_template('adicionar_aluno.html')

# Rota para sair do professor (logout)
@professor_bp.route('/sair', methods=['GET'])
def sair():
    """Realiza o logout do professor."""
    session.clear()  # Limpa a sessão
    flash("Você foi desconectado!", "success")
    return redirect(url_for('login_professor.login_professor'))

from flask import render_template, request, redirect, url_for

def get_aluno_nome(aluno_id):
    db = DBConnection()
    aluno = db.get_one('alunos', 'nome', 'id = ?', [aluno_id])
    return aluno[0] if aluno else None

@professor_bp.route('/confirmar_exclusao/<int:treino_id>/<int:aluno_id>')
def confirmar_exclusao(treino_id, aluno_id):
    db = DBConnection()
    treino = db.get_one('treinos', 'id, nome, descricao', 'id = ?', [treino_id])  # Obter o treino pelo ID
    aluno_nome = get_aluno_nome(aluno_id)  # Função fictícia para obter o nome do aluno
    return render_template('confirmar_exclusao.html', treino=treino, aluno_id=aluno_id, aluno_nome=aluno_nome)

@professor_bp.route('/excluir_treino_confirmado/<int:treino_id>/<int:aluno_id>', methods=['POST'])
def excluir_treino_confirmado(treino_id, aluno_id):
    db = DBConnection()
    db.excluir_treino(treino_id)  # Função fictícia para excluir o treino pelo ID
    flash("Treino excluído com sucesso!", "success")
    return redirect(url_for('professor.treinos_aluno', aluno_id=aluno_id))
