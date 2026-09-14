from enum import StrEnum


class TipoOperacao(StrEnum):
    ATRIBUIR = "atribuir"
    REMOVER = "remover"
    MOVER = "mover"


class RegistroOperacao:
    def __init__(
        self,
        tipo: TipoOperacao,
        turma_id: str,
        professor_matricula: str | None = None,
        professor_anterior_matricula: str | None = None,
    ):
        self.tipo = tipo
        self.turma_id = turma_id
        self.professor_matricula = professor_matricula
        self.professor_anterior_matricula = professor_anterior_matricula

    def __str__(self): ...


class HistoricoAlteracoes:
    def __init__(self):
        self._historico: list[RegistroOperacao] = []
        self._futuro: list[RegistroOperacao] = []

    def registrar(self, registro: RegistroOperacao):
        self._historico.append(registro)
        self._futuro.clear()

    def pode_desfazer(self) -> bool:
        return bool(self._historico)

    def pode_refazer(self) -> bool:
        return bool(self._futuro)

    def desfazer(self) -> RegistroOperacao | None:
        if not self.pode_desfazer():
            return None
        registro = self._historico.pop()
        self._futuro.append(registro)
        return registro

    def refazer(self) -> RegistroOperacao | None:
        if not self.pode_refazer():
            return None
        registro = self._futuro.pop()
        self._historico.append(registro)
        return registro
