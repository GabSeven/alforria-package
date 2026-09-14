# import operacoes

# from .classes import Turma, Professor
from .db.repositorios import RepositorioProfessores, RepositorioTurmas
from .dominio.professor import Professor
from .dominio.turma import Turma
from .excecoes import ProfessorInexistenteError, TurmaInexistenteError
from .historico import HistoricoAlteracoes, RegistroOperacao, TipoOperacao
from .operacoes import atribuir_turma, mover_turma, remover_turma


class Sessao:
    def __init__(
        self,
        professores: RepositorioProfessores,
        turmas: RepositorioTurmas,
        historico: HistoricoAlteracoes | None = None,
    ):
        self.professores = professores
        self.turmas = turmas
        self.historico = historico or HistoricoAlteracoes()

    def desfazer(self) -> RegistroOperacao | None:
        registro = self.historico.desfazer()
        if registro is None:
            return None

        self._aplicar_registro(registro, reverter=True)
        return registro

    def refazer(self) -> RegistroOperacao | None:
        registro = self.historico.refazer()
        if registro is None:
            return None

        self._aplicar_registro(registro, reverter=False)
        return registro

    def _aplicar_registro(self, registro: RegistroOperacao, *, reverter: bool = False):
        turma = self._turma_por_id(registro.turma_id)

        match (registro.tipo, reverter):
            case (TipoOperacao.ATRIBUIR, False):
                p = self._professor_por_matricula(registro.professor_matricula)
                self._aplicar_atribuir(turma, p)
            case (TipoOperacao.ATRIBUIR, True):
                self._aplicar_remover(turma)
            case (TipoOperacao.REMOVER, False):
                self._aplicar_remover(turma)
            case (TipoOperacao.REMOVER, True):
                p = self._professor_por_matricula(registro.professor_anterior_matricula)
                self._aplicar_atribuir(turma, p)
            case (TipoOperacao.MOVER, False):
                p = self._professor_por_matricula(registro.professor_matricula)
                self._aplicar_mover(turma, p)
            case (TipoOperacao.MOVER, True):
                p = self._professor_por_matricula(registro.professor_anterior_matricula)
                self._aplicar_mover(turma, p)

    def atribuir_turma(self, turma_id: str, matricula: str):
        professor = self._professor_por_matricula(matricula)
        turma = self._turma_por_id(turma_id)

        self._aplicar_atribuir(turma, professor)

        registro = RegistroOperacao(TipoOperacao.ATRIBUIR, turma_id, matricula)
        self.historico.registrar(registro)

    def mover_turma(self, turma_id: str, matricula: str):
        professor = self._professor_por_matricula(matricula)
        turma = self._turma_por_id(turma_id)
        professor_anterior = turma.professor

        self._aplicar_mover(turma, professor)

        registro = RegistroOperacao(
            TipoOperacao.MOVER,
            turma_id,
            professor_matricula=matricula,
            professor_anterior_matricula=professor_anterior.matricula,
        )
        self.historico.registrar(registro)

    def remover_turma(self, turma_id: str):
        turma = self._turma_por_id(turma_id)
        professor = turma.professor
        if professor is None:
            return

        self._aplicar_remover(turma)

        registro = RegistroOperacao(
            TipoOperacao.REMOVER,
            turma_id,
            professor_anterior_matricula=professor.matricula,
        )
        self.historico.registrar(registro)

    def _turma_por_id(self, turma_id):
        t = self.turmas.buscar_por_id(turma_id)
        if t is None:
            raise TurmaInexistenteError(turma_id)
        return t

    def _professor_por_matricula(self, matricula):
        p = self.professores.buscar_por_matricula(matricula)
        if p is None:
            raise ProfessorInexistenteError(matricula)
        return p

    def _aplicar_atribuir(self, turma: Turma, professor: Professor):
        atribuir_turma(turma, professor)
        self.turmas.salvar(turma)

    def _aplicar_remover(self, turma: Turma):
        remover_turma(turma)
        self.turmas.salvar(turma)

    def _aplicar_mover(self, turma: Turma, professor: Professor):
        mover_turma(turma, professor)
        self.turmas.salvar(turma)
