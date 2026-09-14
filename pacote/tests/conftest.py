import pytest
from alforria.db.modelos import Base
from alforria.db.repositorios import (
    BancoMemoria,
    RepositorioProfessoresMemoria,
    RepositorioProfessoresSQL,
    RepositorioTurmasMemoria,
    RepositorioTurmasSQL,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessaoSQL = sessionmaker(bind=engine)

    with SessaoSQL() as s:
        yield s


@pytest.fixture(params=["sql", "memoria"])
def modo(request):
    return request.param


@pytest.fixture
def banco():
    return BancoMemoria()


@pytest.fixture
def repo_professores(modo, session, banco):
    if modo == "sql":
        return RepositorioProfessoresSQL(session)
    return RepositorioProfessoresMemoria(banco)


@pytest.fixture
def repo_turmas(modo, session, banco):
    if modo == "sql":
        return RepositorioTurmasSQL(session)
    return RepositorioTurmasMemoria(banco)
