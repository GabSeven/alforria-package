from alforria.db.repositorios import RepositorioProfessores, RepositorioTurmas
from alforria.dominio.professor import Professor
from alforria.dominio.turma import Turma


def test_atribuir_turma_aparece_na_lista_professor(
    repo_professores: RepositorioProfessores, repo_turmas: RepositorioTurmas
):
    p = Professor(matricula="p1", nome_completo="Professor 1")
    repo_professores.salvar(p)

    t = Turma(nome="t1", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    t.add_professor(p)
    repo_turmas.salvar(t)

    p_encontrado = repo_professores.buscar_por_matricula("p1")

    assert len(p_encontrado.turmas_a_lecionar) == 1
    assert p_encontrado.turmas_a_lecionar[0].id == t.id


def test_buscar_turma_traz_professor_associado(
    repo_professores: RepositorioProfessores, repo_turmas: RepositorioTurmas
):
    p = Professor(matricula="p1", nome_completo="Professor 1")
    repo_professores.salvar(p)

    t = Turma(nome="t1", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    t.add_professor(p)
    repo_turmas.salvar(t)

    t_encontrada = repo_turmas.buscar_por_id(t.id)

    assert t_encontrada.professor.matricula == "p1"


def test_turma_sem_professor_nao_aparece_em_nenhuma_lista_de_professor(
    repo_professores: RepositorioProfessores, repo_turmas: RepositorioTurmas
):
    p = Professor(matricula="p1", nome_completo="Professor 1")
    repo_professores.salvar(p)

    t = Turma(nome="t1", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    repo_turmas.salvar(t)

    t_encontrada = repo_turmas.buscar_por_id(t.id)
    p_encontrado = repo_professores.buscar_por_matricula("p1")

    assert t_encontrada.professor is None
    assert len(p_encontrado.turmas_a_lecionar) == 0


def test_professor_com_multiplas_turmas_retorna_todas(
    repo_professores: RepositorioProfessores, repo_turmas: RepositorioTurmas
):
    p = Professor(matricula="p1", nome_completo="Professor 1")
    repo_professores.salvar(p)

    t1 = Turma(nome="t1", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    t2 = Turma(nome="t2", codigo_disc="FIS101", numero_turma=1, semestralidade=2)
    for t in (t1, t2):
        t.add_professor(p)
        repo_turmas.salvar(t)

    p_encontrado = repo_professores.buscar_por_matricula("p1")

    assert len(p_encontrado.turmas_a_lecionar) == 2
    assert {t.id for t in p_encontrado.turmas_a_lecionar} == {t1.id, t2.id}


def test_remover_turma_do_professor_reflete_no_banco(
    repo_professores: RepositorioProfessores, repo_turmas: RepositorioTurmas
):
    p = Professor(matricula="p1", nome_completo="Professor 1")
    repo_professores.salvar(p)

    t = Turma(nome="t1", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    t.add_professor(p)
    repo_turmas.salvar(t)

    t.remove_professor()
    repo_turmas.salvar(t)

    t_encontrada = repo_turmas.buscar_por_id("MAT101_1_1")
    assert t_encontrada.professor is None
    p_encontrado = repo_professores.buscar_por_matricula("p1")
    assert p_encontrado.turmas_a_lecionar == []


def test_mover_turma_entre_professores(
    repo_professores: RepositorioProfessores, repo_turmas: RepositorioTurmas
):
    p1 = Professor(matricula="p1", nome_completo="Professor 1")
    p2 = Professor(matricula="p2", nome_completo="Professor 2")
    repo_professores.salvar(p1)
    repo_professores.salvar(p2)

    t = Turma(nome="t1", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    t.add_professor(p1)
    repo_turmas.salvar(t)

    t.remove_professor()
    t.add_professor(p2)
    repo_turmas.salvar(t)

    t_encontrada = repo_turmas.buscar_por_id("MAT101_1_1")
    assert t_encontrada.professor.matricula == p2.matricula

    p1_encontrado = repo_professores.buscar_por_matricula("p1")
    p2_encontrado = repo_professores.buscar_por_matricula("p2")
    assert p1_encontrado.turmas_a_lecionar == []
    assert len(p2_encontrado.turmas_a_lecionar) == 1
    assert p2_encontrado.turmas_a_lecionar[0].id == t.id == "MAT101_1_1"


def test_mutar_turma_sem_salvar_nao_altera_repositorio(
    repo_professores: RepositorioProfessores, repo_turmas: RepositorioTurmas
):
    p1 = Professor(matricula="p1", nome_completo="Professor 1")
    p2 = Professor(matricula="p2", nome_completo="Professor 2")
    repo_professores.salvar(p1)
    repo_professores.salvar(p2)

    t = Turma(nome="t1", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    t.add_professor(p1)
    repo_turmas.salvar(t)

    t.remove_professor()
    t.add_professor(p2)

    t_encontrada = repo_turmas.buscar_por_id("MAT101_1_1")
    assert t_encontrada.professor.matricula == p1.matricula == "p1"


def test_mutar_professor_sem_salvar_nao_altera_relacao(
    repo_professores: RepositorioProfessores, repo_turmas: RepositorioTurmas
):
    p = Professor(matricula="p1", nome_completo="Professor 1")
    repo_professores.salvar(p)

    t = Turma(nome="t1", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    p.add_course(t)
    repo_turmas.salvar(t)

    p.remove_course(t)

    p_encontrado = repo_professores.buscar_por_matricula("p1")

    assert len(p_encontrado.turmas_a_lecionar) == 1
    assert p_encontrado.turmas_a_lecionar[0].id == t.id == "MAT101_1_1"
