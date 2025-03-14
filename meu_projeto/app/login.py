import jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import Aluno
from config import SessionLocal, gerar_hash_senha  # Certifique-se de importar a função 'gerar_hash_senha' do arquivo correto

# Função para verificar a senha e gerar o token
def login_usuario(email, senha):
    db = SessionLocal()
    usuario = db.query(Aluno).filter(Aluno.email == email).first()

    if usuario and usuario.senha == gerar_hash_senha(senha):
        # Gerar token JWT
        token = gerar_token(usuario.id)
        db.close()
        print(f"Login bem-sucedido! Token: {token}")
        return token
    else:
        db.close()
        print("Credenciais inválidas!")
        return None

# Função para gerar o token JWT
def gerar_token(usuario_id):
    expira_em = datetime.utcnow() + timedelta(hours=1)
    token = jwt.encode({"usuario_id": usuario_id, "exp": expira_em}, "sua_chave_secreta", algorithm="HS256")
    return token
