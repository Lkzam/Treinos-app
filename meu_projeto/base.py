import pyodbc

class DBConnection:
    def __init__(self):
        self.conn_str = (
            r'DRIVER={ODBC Driver 17 for SQL Server};'
            r'SERVER=localhost;'
            r'DATABASE=DaniRibeiro;'
            r'Trusted_Connection=yes;'
        )

    def connect(self):
        """Cria e retorna uma conexão com o banco de dados."""
        try:
            print("Tentando conectar ao banco de dados...")
            return pyodbc.connect(self.conn_str)
        except pyodbc.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            raise

    def execute_query(self, query, params=None):
        """Executa INSERT, UPDATE, DELETE e confirma a transação."""
        with self.connect() as conn:
            cursor = conn.cursor()
            print(f"Executando query: {query} com parâmetros: {params}")
            cursor.execute(query, params or [])
            conn.commit()

    def fetchall(self, query, params=None):
        """Executa um SELECT e retorna todos os resultados."""
        with self.connect() as conn:
            cursor = conn.cursor()
            print(f"Executando query: {query} com parâmetros: {params}")
            cursor.execute(query, params or [])
            return cursor.fetchall()

    def fetchone(self, query, params=None):
        """Executa um SELECT e retorna um único resultado."""
        with self.connect() as conn:
            cursor = conn.cursor()
            print(f"Executando query: {query} com parâmetros: {params}")
            cursor.execute(query, params or [])
            return cursor.fetchone()

    def count(self, table):
        """Conta o número de registros em uma tabela."""
        query = f"SELECT COUNT(*) FROM {table}"
        result = self.fetchone(query)
        return result[0] if result else 0

    def get_all(self, table_name, columns="*", condition=None):
        """Obtém todos os registros de uma tabela com colunas específicas."""
        query = f"SELECT {columns} FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        return self.fetchall(query)

    def get_one(self, table_name, columns="*", condition=None, params=None):
        """Obtém um único registro de uma tabela."""
        query = f"SELECT {columns} FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        return self.fetchone(query, params)

    # --- MÉTODOS PARA PROFESSOR ---
    
    def professor_login(self, email, senha):
        """Autentica um professor verificando a senha."""
        query = "SELECT id, nome FROM professores WHERE email = ? AND senha = ?"
        result = self.fetchone(query, [email, senha])
        return {"id": result[0], "nome": result[1]} if result else None

    def professor_register(self, nome, email, senha, especialidade):
        """Registra um novo professor no banco de dados."""
        query = "INSERT INTO professores (nome, email, senha, especialidade) VALUES (?, ?, ?, ?)"
        try:
            print(f"Tentando registrar professor: {nome}, {email}, {senha}, {especialidade}")
            self.execute_query(query, [nome, email, senha, especialidade])
            print(f"Professor {nome} registrado com sucesso!")
        except Exception as e:
            print(f"Erro ao registrar professor: {e}")

    # --- MÉTODO PARA ALUNO ---
    
    def aluno_login(self, email, senha):
        """Autentica um aluno verificando o email e senha."""
        query = "SELECT id, nome FROM alunos WHERE email = ? AND senha = ?"
        result = self.fetchone(query, [email, senha])
        return {"id": result[0], "nome": result[1]} if result else None

    def buscar_treinos_aluno(self, aluno_id):
        """Recupera os treinos vinculados a um aluno específico."""
        query = "SELECT id, nome, descricao FROM treinos WHERE aluno_id = ?"
        return self.fetchall(query, [aluno_id])

    def criar_treino(self, nome, descricao, aluno_id):
        """Cria um novo treino para um aluno específico."""
        query = "INSERT INTO treinos (nome, descricao, aluno_id) VALUES (?, ?, ?)"
        self.execute_query(query, [nome, descricao, aluno_id])

    def editar_treino(self, treino_id, nome, descricao):
        """Atualiza um treino existente."""
        query = "UPDATE treinos SET nome = ?, descricao = ? WHERE id = ?"
        self.execute_query(query, [nome, descricao, treino_id])

    def excluir_treino(self, treino_id):
        """Exclui um treino existente."""
        query = "DELETE FROM treinos WHERE id = ?"
        self.execute_query(query, [treino_id])

    def get_aluno_by_id(self, aluno_id):
        """Recupera um aluno pelo seu ID."""
        query = "SELECT nome, email FROM alunos WHERE id = ?"
        result = self.fetchone(query, [aluno_id])
        return result if result else None

    def aluno_register(self, nome, email, senha):
        """Registra um novo aluno no banco de dados."""
        query = "INSERT INTO alunos (nome, email, senha) VALUES (?, ?, ?)"
        self.execute_query(query, [nome, email, senha])

    def aluno_existe(self, email):
        """Verifica se um aluno com o e-mail fornecido já existe."""
        query = "SELECT COUNT(*) FROM alunos WHERE email = ?"
        result = self.fetchone(query, [email])
        return result[0] > 0 if result else False

    # --- MÉTODO PARA ASSOCIAÇÃO DE ALUNO A PROFESSOR ---
    
    def associar_aluno_professor(self, aluno_id, professor_id):
        """Associa um aluno ao professor específico."""
        # Verifica se o aluno existe
        aluno_existe = self.get_one('alunos', 'id', 'id = ?', [aluno_id])
        if not aluno_existe:
            print(f"Erro: Aluno com ID {aluno_id} não existe.")
            return False

        # Verifica se o professor existe
        professor_existe = self.get_one('professores', 'id', 'id = ?', [professor_id])
        if not professor_existe:
            print(f"Erro: Professor com ID {professor_id} não existe.")
            return False

        query = "INSERT INTO alunos_professores (aluno_id, professor_id) VALUES (?, ?)"
        try:
            print(f"Tentando associar aluno_id: {aluno_id} com professor_id: {professor_id}")  # Log para verificar os IDs
            self.execute_query(query, [aluno_id, professor_id])
            print("Associação realizada com sucesso!")  # Log de sucesso
            return True
        except Exception as e:
            print(f"Erro ao associar aluno ao professor: {e}")  # Log de erro
            return False
