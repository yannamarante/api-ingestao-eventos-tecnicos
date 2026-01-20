from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

metadata = MetaData()


def criar_engine(url_banco: str):
    return create_engine(url_banco, pool_pre_ping=True)


def criar_fabrica_sessoes(engine):
    return scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))
