from config import SessionLocal
from models import Treino
from datetime import datetime

# Função para criar um treino
def criar_treino(aluno_id, exercicios):
    if not isinstance(aluno_id, int):  # Verifica se é um número inteiro
        print("Erro: ID do aluno inválido.")
        return None

    db = SessionLocal()
    novo_treino = Treino(
        aluno_id=aluno_id,
        exercicios=exercicios,
        data_criacao=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    )

    db.add(novo_treino)
    db.commit()
    db.refresh(novo_treino)
    db.close()

    print(f"Treino criado para o aluno ID {aluno_id} com sucesso!")
    return novo_treino
