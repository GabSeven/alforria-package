from copy import deepcopy
from typing import Protocol

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..classes import Professor, Turma
from .conversao import (
    professor_para_dominio,
    professor_para_orm,
    turma_para_dominio,
    turma_para_orm,
)
from .modelos import ProfessorORM, TurmaORM


class BancoMemoria:
    def __init__(self):
        self.professores: dict[str, Professor] = {}
        self.turmas: dict[str, Turma] = {}


class RepositorioTurmas(Protocol):
    def buscar_por_id(self, id: str) -> Turma | None: ...
    def salvar(self, turma: Turma) -> None: ...
    def listar(
        self, *, semestralidade: int | None = None, com_professor: bool | None = None
    ) -> list[Turma]: ...


class RepositorioTurmasSQL(RepositorioTurmas):
    def __init__(self, session: Session):
        self._session = session

    def buscar_por_id(self, id: str) -> Turma | None:
        orm = self._session.get(TurmaORM, id)
        return turma_para_dominio(orm) if orm is not None else None

    def salvar(self, turma: Turma) -> None:
        orm = turma_para_orm(turma)
        self._session.merge(orm)

    def listar(
        self, *, semestralidade: int | None = None, com_professor: bool | None = None
    ) -> list[Turma]:
        stmt = select(TurmaORM)

        if semestralidade is not None:
            stmt = stmt.where(TurmaORM.semestralidade == semestralidade)

        if com_professor is True:
            stmt = stmt.where(TurmaORM.professor_matricula.is_not(None))
        elif com_professor is False:
            stmt = stmt.where(TurmaORM.professor_matricula.is_(None))

        orms = self._session.scalars(stmt).all()
        return [turma_para_dominio(orm) for orm in orms]


class RepositorioTurmasMemoria(RepositorioTurmas):
    def __init__(self, banco: BancoMemoria | None = None):
        self._banco = banco or BancoMemoria()
        self._dados = self._banco.turmas

    def buscar_por_id(self, id: str) -> Turma | None:
        t = self._dados.get(id)
        return deepcopy(t) if t is not None else None

    def salvar(self, turma: Turma) -> None:
        self._dados[turma.id] = deepcopy(turma)

    def listar(
        self, *, semestralidade: int | None = None, com_professor: bool | None = None
    ) -> list[Turma]:
        resultado = list(self._dados.values())

        if semestralidade is not None:
            resultado = [t for t in resultado if t.semestralidade == semestralidade]

        if com_professor is True:
            resultado = [t for t in resultado if t.professor is not None]
        elif com_professor is False:
            resultado = [t for t in resultado if t.professor is None]

        return [deepcopy(t) for t in resultado]


class RepositorioProfessores(Protocol):
    def buscar_por_matricula(self, matricula: str) -> Professor | None: ...
    def salvar(self, professor: Professor) -> None: ...
    def listar(self, temporario: bool | None = None) -> list[Professor]: ...


class RepositorioProfessoresSQL(RepositorioProfessores):
    def __init__(self, session: Session):
        self._session = session

    def buscar_por_matricula(self, matricula: str) -> Professor | None:
        orm = self._session.get(ProfessorORM, matricula)
        return professor_para_dominio(orm) if orm is not None else None

    def salvar(self, professor: Professor) -> None:
        orm = professor_para_orm(professor)
        self._session.merge(orm)

    def listar(self, temporario: bool | None = None) -> list[Professor]:
        stmt = select(ProfessorORM)

        if temporario is not None:
            stmt = stmt.where(ProfessorORM.temporario == temporario)

        orms = self._session.scalars(stmt).all()
        return [professor_para_dominio(orm) for orm in orms]


class RepositorioProfessoresMemoria(RepositorioProfessores):
    def __init__(self, banco: BancoMemoria | None = None):
        self._banco = banco or BancoMemoria()
        self._dados = self._banco.professores

    def buscar_por_matricula(self, matricula: str) -> Professor | None:
        p = self._dados.get(matricula, None)
        if p is None:
            return None

        p = deepcopy(p)
        mapa = self._indice_turmas_por_matricula()
        p.turmas_a_lecionar = [deepcopy(t) for t in mapa.get(matricula, [])]
        return p

    def salvar(self, professor: Professor):
        self._dados[professor.matricula] = deepcopy(professor)

    def listar(self, temporario: bool | None = None) -> list[Professor]:
        resultado = list(self._dados.values())

        if temporario is not None:
            resultado = [p for p in resultado if p.temporario == temporario]

        resultado = [deepcopy(p) for p in resultado]

        mapa = self._indice_turmas_por_matricula()

        for p in resultado:
            p.turmas_a_lecionar = mapa.get(p.matricula, [])
        return resultado

    def _turmas_de(self, matricula: str) -> list[Turma]:
        return [
            deepcopy(t)
            for t in self._banco.turmas.values()
            if t.professor is not None and t.professor.matricula == matricula
        ]

    def _indice_turmas_por_matricula(self) -> dict[str, list[Turma]]:
        mapa: dict[str, list[Turma]] = {}
        for t in self._banco.turmas.values():
            if t.professor is not None:
                mapa.setdefault(t.professor.matricula, []).append(t)
        return mapa
