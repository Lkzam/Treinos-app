from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


# Configuração da URL de conexão com o SQL Server
DATABASE_URL = "mssql+pyodbc://sa:1234@localhost/DaniRibeiro?driver=ODBC+Driver+17+for+SQL+Server"

# Criar a engine de conexão com o banco de dados
engine = create_engine(DATABASE_URL, echo=True)

# Criar a sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Definir a base para os modelos
Base = declarative_base()
