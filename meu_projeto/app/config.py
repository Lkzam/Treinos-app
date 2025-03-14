from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base as orm_declarative_base
from app.engine import engine, Base  # Importando o 'engine' e 'Base' de 'engine.py'


# Configuração da URL de conexão com o SQL Server
DATABASE_URL = "mssql+pyodbc://sa:1234@localhost/DaniRibeiro?driver=ODBC+Driver+17+for+SQL+Server"

# Criar a engine de conexão
engine = create_engine(DATABASE_URL, echo=True)

# Criar a sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criação das tabelas no banco de dados
Base.metadata.create_all(bind=engine)
