# database.py
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Carregue as variáveis de ambiente conforme sua configuração
DATABASE_USER = os.getenv("DATABASE_USER", "postgres")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "balcao")
DATABASE_HOST = os.getenv("DATABASE_HOST", "db")  # nome do serviço no docker-compose
DATABASE_PORT = os.getenv("DATABASE_PORT", "5432")
DATABASE_NAME = os.getenv("DATABASE_NAME", "pets_db")  # ou outro nome conforme o serviço

# URL de conexão para PostgreSQL com asyncpg
DATABASE_URL = (
    f"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
)

# Criação do engine assíncrono
engine = create_async_engine(DATABASE_URL, echo=True)

# Sessão assíncrona para injeção de dependências nos endpoints
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


