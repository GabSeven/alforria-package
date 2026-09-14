from .dominio.professor import Professor
from .dominio.turma import Turma


class AlforriaError(Exception): ...


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


class TurmaInexistenteError(AlforriaError):
    def __init__(self, turma_id: str):
        super().__init__(f"Turma {turma_id} não encontrada.")


class ProfessorInexistenteError(AlforriaError):
    def __init__(self, matricula: str):
        super().__init__(f"Professor {matricula} não encontrado.")
