from .dominio.professor import Professor
from .dominio.turma import Turma
from .excecoes import AlforriaError


class TurmaJaAtribuidaError(AlforriaError):
    def __init__(self, turma: Turma, professor: Professor):
        atual = turma.professor
        super().__init__(
            f"Turma {turma.id} já atribuída a {atual.nome()} "
            f"(não a {professor.nome()})."
        )


class TurmaSemProfessorError(AlforriaError):
    def __init__(self, turma: Turma):
        super().__init__(f"Turma {turma.id} não tem professor.")


def atribuir_turma(turma: Turma, professor: Professor) -> None:
    if turma.professor is not None:
        if turma.professor == professor:
            return

        raise TurmaJaAtribuidaError(turma, professor)

    professor.add_course(turma)
    turma.add_professor(professor)


def remover_turma(turma: Turma) -> None:
    turma.remove_professor()


def mover_turma(turma: Turma, professor: Professor) -> None:
    if turma.professor is None:
        raise TurmaSemProfessorError(turma)

    turma.remove_professor()
    turma.add_professor(professor)
