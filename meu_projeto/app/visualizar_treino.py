from flask import Flask, render_template, request
from app.config import SessionLocal  # Importe o SessionLocal do config.py
from app.models import Aluno, Treino
import jwt  # Assumindo que você vai usar JWT para decodificação de token
from datetime import datetime

app = Flask(__name__)

@app.route('/aluno/treinos')
def visualizar_treinos():
    token = request.args.get('token')
    
    if not token:
        return "Token não fornecido", 400
    
    # Decodificar o token para obter o ID do aluno
    try:
        secret_key = 'sua_chave_secreta'  # Altere para sua chave secreta
        decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
        aluno_id = decoded_token['id']
    except jwt.ExpiredSignatureError:
        return "Token expirado", 401
    except jwt.InvalidTokenError:
        return "Token inválido", 401
    
    db = SessionLocal()
    try:
        aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
        
        if aluno:
            treinos = db.query(Treino).filter(Treino.aluno_id == aluno.id).all()
            return render_template('treinos.html', aluno_nome=aluno.nome, treinos=treinos)
        else:
            return "Aluno não encontrado", 404
    finally:
        db.close()
