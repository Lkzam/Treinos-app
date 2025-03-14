from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.config import Base

# Modelo Aluno
class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    senha = Column(String)

    treinos = relationship("Treino", back_populates="aluno")

# Modelo Treino
class Treino(Base):
    __tablename__ = 'treinos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    aluno_id = Column(Integer, ForeignKey('alunos.id'), nullable=False)

    aluno = relationship('Aluno', back_populates='treinos')

# Função para gerar hash de senha
import hashlib

def gerar_hash_senha(senha):
    return hashlib.sha256(senha.encode('utf-8')).hexdigest()
