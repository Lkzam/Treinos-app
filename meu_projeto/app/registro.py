import hashlib
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.exc import IntegrityError
from config import SessionLocal

Base = declarative_base()

class Aluno(Base):
    __tablename__ = 'alunos'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    senha = Column(String)

class Professor(Base):
    __tablename__ = 'professores'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    email = Column(String, unique=True, index=True)

# Função para gerar o hash da senha
def gerar_hash_senha(senha):
    return hashlib.sha256(senha.encode('utf-8')).hexdigest()

# Função para registrar um aluno
def registrar_aluno(nome, email, senha):
    db = SessionLocal()
    try:
        if db.query(Aluno).filter(Aluno.email == email).first():
            print("E-mail já registrado!")
            return

        hashed_senha = gerar_hash_senha(senha)
        novo_aluno = Aluno(nome=nome, email=email, senha=hashed_senha)
        db.add(novo_aluno)
        db.commit()
        db.refresh(novo_aluno)
        print(f"Aluno {nome} registrado com sucesso!")
    except IntegrityError:
        db.rollback()
        print("Erro: E-mail já registrado!")
    except Exception as e:
        print(f"Erro ao registrar aluno: {e}")
    finally:
        db.close()

# Função para registrar um professor
def registrar_professor(nome, email):
    db = SessionLocal()
    try:
        if db.query(Professor).filter(Professor.email == email).first():
            print("E-mail já registrado!")
            return

        novo_professor = Professor(nome=nome, email=email)
        db.add(novo_professor)
        db.commit()
        db.refresh(novo_professor)
        print(f"Professor {nome} registrado com sucesso!")
    except IntegrityError:
        db.rollback()
        print("Erro: E-mail já registrado!")
    except Exception as e:
        print(f"Erro ao registrar professor: {e}")
    finally:
        db.close()
