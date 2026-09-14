from alforria import Professor, Turma
from alforria.db.repositorios import RepositorioProfessores, RepositorioTurmas
from alforria.operacoes import (
    TurmaJaAtribuidaError,
    TurmaSemProfessorError,
    atribuir_turma,
)
from alforria.sessao import ProfessorInexistenteError, Sessao, TurmaInexistenteError
from pytest import raises


def test_atribuir_persiste_e_sincroniza_os_dois_lados(
    repo_professores: RepositorioProfessores, repo_turmas: RepositorioTurmas
):
    p = Professor(matricula="p1", nome_completo="Professor 1")
    repo_professores.salvar(p)

    t = Turma(nome="Matemática", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    repo_turmas.salvar(t)

    sessao = Sessao(repo_professores, repo_turmas)
    sessao.atribuir_turma(t.id, "p1")

    t_encontrada = repo_turmas.buscar_por_id(t.id)
    assert t_encontrada.professor is not None
    assert t_encontrada.professor.matricula == "p1"

    p_encontrado = repo_professores.buscar_por_matricula("p1")
    assert len(p_encontrado.turmas_a_lecionar) == 1
    assert p_encontrado.turmas_a_lecionar[0].id == t.id


def test_atribuir_turma_inexistente_levanta_erro(
    repo_professores: RepositorioProfessores, repo_turmas: RepositorioTurmas
):
    p = Professor(matricula="p1", nome_completo="Professor 1")
    repo_professores.salvar(p)

    sessao = Sessao(repo_professores, repo_turmas)
    with raises(TurmaInexistenteError):
        sessao.atribuir_turma("turma inexistente", "p1")


def test_atribuir_professor_inexistente_levanta_erro(
    repo_professores: RepositorioProfessores, repo_turmas: RepositorioTurmas
):
    t = Turma(nome="Matemática", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    repo_turmas.salvar(t)

    sessao = Sessao(repo_professores, repo_turmas)
    with raises(ProfessorInexistenteError):
        sessao.atribuir_turma(t.id, "Professor Inexistente")


def test_atribuir_turma_com_outro_dono_levanta_erro(
    repo_professores: RepositorioProfessores, repo_turmas: RepositorioTurmas
):
    p1 = Professor(matricula="p1", nome_completo="Professor 1")
    p2 = Professor(matricula="p2", nome_completo="Professor 2")
    repo_professores.salvar(p1)
    repo_professores.salvar(p2)

    t = Turma(nome="Matemática", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    atribuir_turma(t, p1)
    repo_turmas.salvar(t)

    sessao = Sessao(repo_professores, repo_turmas)
    with raises(TurmaJaAtribuidaError):
        sessao.atribuir_turma(t.id, "p2")

    assert not sessao.historico.pode_desfazer()
    assert sessao.desfazer() is None


def test_remover_desassocia_e_persiste(
    repo_professores: RepositorioProfessores, repo_turmas: RepositorioTurmas
):
    p = Professor(matricula="p1", nome_completo="Professor 1")
    repo_professores.salvar(p)

    t = Turma(nome="Matemática", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    repo_turmas.salvar(t)

    sessao = Sessao(repo_professores, repo_turmas)
    sessao.atribuir_turma(t.id, "p1")
    sessao.remover_turma(t.id)

    t_encontrada = repo_turmas.buscar_por_id(t.id)
    assert t_encontrada.professor is None

    p_encontrado = repo_professores.buscar_por_matricula("p1")
    assert p_encontrado.turmas_a_lecionar == []


def test_remover_turma_sem_professor_nao_registra_historico(
    repo_professores: RepositorioProfessores, repo_turmas: RepositorioTurmas
):
    t = Turma(nome="Matemática", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    repo_turmas.salvar(t)

    sessao = Sessao(repo_professores, repo_turmas)
    sessao.remover_turma(t.id)

    assert not sessao.historico.pode_desfazer()


def test_mover_entre_professores_persiste(
    repo_professores: RepositorioProfessores, repo_turmas: RepositorioTurmas
):
    p1 = Professor(matricula="p1", nome_completo="Professor 1")
    p2 = Professor(matricula="p2", nome_completo="Professor 2")
    repo_professores.salvar(p1)
    repo_professores.salvar(p2)

    t = Turma(nome="Matemática", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    atribuir_turma(t, p1)
    repo_turmas.salvar(t)

    sessao = Sessao(repo_professores, repo_turmas)
    sessao.mover_turma(t.id, "p2")

    t_encontrada = repo_turmas.buscar_por_id(t.id)
    assert t_encontrada.professor is not None
    assert t_encontrada.professor.matricula == "p2"

    p1_encontrado = repo_professores.buscar_por_matricula("p1")
    assert p1_encontrado.turmas_a_lecionar == []
    p2_encontrado = repo_professores.buscar_por_matricula("p2")
    assert len(p2_encontrado.turmas_a_lecionar) == 1
    assert p2_encontrado.turmas_a_lecionar[0].id == t.id


def test_mover_sem_dono_levanta_erro(
    repo_professores: RepositorioProfessores, repo_turmas: RepositorioTurmas
):
    p = Professor(matricula="p1", nome_completo="Professor 1")
    repo_professores.salvar(p)

    t = Turma(nome="Matemática", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    repo_turmas.salvar(t)

    sessao = Sessao(repo_professores, repo_turmas)
    with raises(TurmaSemProfessorError):
        sessao.mover_turma(t.id, "p1")


def test_desfazer_atribuir_reverte_e_persiste(
    repo_professores: RepositorioProfessores, repo_turmas: RepositorioTurmas
):
    p = Professor(matricula="p1", nome_completo="Professor 1")
    repo_professores.salvar(p)

    t = Turma(nome="Matemática", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    repo_turmas.salvar(t)

    sessao = Sessao(repo_professores, repo_turmas)
    sessao.atribuir_turma(t.id, "p1")
    sessao.desfazer()

    t_encontrada = repo_turmas.buscar_por_id(t.id)
    assert t_encontrada.professor is None

    p_encontrado = repo_professores.buscar_por_matricula("p1")
    assert p_encontrado.turmas_a_lecionar == []


def test_desfazer_remover_restaura_professor(
    repo_professores: RepositorioProfessores, repo_turmas: RepositorioTurmas
):
    p = Professor(matricula="p1", nome_completo="Professor 1")
    repo_professores.salvar(p)

    t = Turma(nome="Matemática", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    atribuir_turma(t, p)
    repo_turmas.salvar(t)

    sessao = Sessao(repo_professores, repo_turmas)
    sessao.remover_turma(t.id)
    sessao.desfazer()

    t_encontrada = repo_turmas.buscar_por_id(t.id)
    assert t_encontrada.professor is not None
    assert t_encontrada.professor.matricula == p.matricula == "p1"

    p_encontrado = repo_professores.buscar_por_matricula("p1")
    assert len(p_encontrado.turmas_a_lecionar) == 1
    assert p_encontrado.turmas_a_lecionar[0].id == t.id


def test_desfazer_mover_retorna_origem(
    repo_professores: RepositorioProfessores, repo_turmas: RepositorioTurmas
):
    p1 = Professor(matricula="p1", nome_completo="Professor 1")
    p2 = Professor(matricula="p2", nome_completo="Professor 2")
    repo_professores.salvar(p1)
    repo_professores.salvar(p2)

    t = Turma(nome="Matemática", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    atribuir_turma(t, p1)
    repo_turmas.salvar(t)

    sessao = Sessao(repo_professores, repo_turmas)
    sessao.mover_turma(t.id, "p2")
    sessao.desfazer()

    t_encontrada = repo_turmas.buscar_por_id(t.id)
    assert t_encontrada.professor is not None
    assert t_encontrada.professor.matricula == "p1"

    p1_encontrado = repo_professores.buscar_por_matricula("p1")
    assert len(p1_encontrado.turmas_a_lecionar) == 1
    assert p1_encontrado.turmas_a_lecionar[0].id == t.id
    p2_encontrado = repo_professores.buscar_por_matricula("p2")
    assert p2_encontrado.turmas_a_lecionar == []


def test_refazer_aplica_novamente(
    repo_professores: RepositorioProfessores, repo_turmas: RepositorioTurmas
):
    p = Professor(matricula="p1", nome_completo="Professor 1")
    repo_professores.salvar(p)

    t = Turma(nome="Matemática", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    repo_turmas.salvar(t)

    sessao = Sessao(repo_professores, repo_turmas)
    sessao.atribuir_turma(t.id, "p1")
    sessao.desfazer()
    sessao.refazer()

    t_encontrada = repo_turmas.buscar_por_id(t.id)
    assert t_encontrada.professor is not None
    assert t_encontrada.professor.matricula == "p1"

    p_encontrado = repo_professores.buscar_por_matricula("p1")
    assert len(p_encontrado.turmas_a_lecionar) == 1
    assert p_encontrado.turmas_a_lecionar[0].id == t.id


def test_desfazer_sem_historico_retorna_none(
    repo_professores: RepositorioProfessores, repo_turmas: RepositorioTurmas
):
    sessao = Sessao(repo_professores, repo_turmas)

    assert sessao.desfazer() is None
    assert sessao.refazer() is None
