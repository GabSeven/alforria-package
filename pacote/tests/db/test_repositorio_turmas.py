from alforria import Professor, Turma
from alforria.db.repositorios import RepositorioProfessores, RepositorioTurmas


def test_salvar_e_buscar_por_id(repo_turmas: RepositorioTurmas):
    t = Turma(nome="Cálculo 1", codigo_disc="1", numero_turma=1, semestralidade=1)
    repo_turmas.salvar(t)

    encontrada = repo_turmas.buscar_por_id("1_1_1")

    assert encontrada is not None
    assert encontrada.nome == "Cálculo 1"


def test_buscar_inexistente_retorna_none(repo_turmas: RepositorioTurmas):
    assert repo_turmas.buscar_por_id("nao existe") is None


def test_salvar_atualiza_turma_existente(repo_turmas: RepositorioTurmas):
    t = Turma(nome="Cálculo 1", codigo_disc="1", numero_turma=1, semestralidade=1)
    repo_turmas.salvar(t)

    t.nome = "Cálculo Avançado"
    repo_turmas.salvar(t)

    encontrada = repo_turmas.buscar_por_id("1_1_1")

    assert encontrada is not None
    assert encontrada.nome == "Cálculo Avançado"


def test_listar_todas_as_turmas(repo_turmas: RepositorioTurmas):
    t1 = Turma(nome="Cálculo", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    t2 = Turma(nome="Física", codigo_disc="FIS101", numero_turma=1, semestralidade=2)
    t3 = Turma(nome="Álgebra", codigo_disc="ALG101", numero_turma=2, semestralidade=2)

    repo_turmas.salvar(t1)
    repo_turmas.salvar(t2)
    repo_turmas.salvar(t3)

    encontradas = repo_turmas.listar()

    assert len(encontradas) == 3
    assert any(t.id == "MAT101_1_1" for t in encontradas)
    assert any(t.id == "FIS101_1_2" for t in encontradas)
    assert any(t.id == "ALG101_2_2" for t in encontradas)


def test_salvar_duas_vezes_nao_duplica(repo_turmas: RepositorioTurmas):
    t1 = Turma(nome="Cálculo", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    repo_turmas.salvar(t1)
    repo_turmas.salvar(t1)

    encontradas = repo_turmas.listar()

    assert len(encontradas) == 1
    assert encontradas[0].id == "MAT101_1_1"


def test_salvar_turma_sem_professor(repo_turmas: RepositorioTurmas):
    t1 = Turma(nome="Cálculo", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    repo_turmas.salvar(t1)

    encontrada = repo_turmas.buscar_por_id("MAT101_1_1")

    assert encontrada is not None
    assert encontrada.professor is None


def test_listar_vazio_retorna_lista_vazia(repo_turmas: RepositorioTurmas):
    encontradas = repo_turmas.listar()

    assert len(encontradas) == 0


def test_listar_filtra_por_semestralidade(repo_turmas: RepositorioTurmas):
    t1 = Turma(nome="Cálculo", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    t2 = Turma(nome="Física", codigo_disc="FIS101", numero_turma=1, semestralidade=2)
    t3 = Turma(nome="Álgebra", codigo_disc="ALG101", numero_turma=2, semestralidade=2)

    repo_turmas.salvar(t1)
    repo_turmas.salvar(t2)
    repo_turmas.salvar(t3)

    semestralidade1 = repo_turmas.listar(semestralidade=1)
    semestralidade2 = repo_turmas.listar(semestralidade=2)

    assert len(semestralidade1) == 1
    assert semestralidade1[0].id == "MAT101_1_1"
    assert len(semestralidade2) == 2
    assert any(t.id == "FIS101_1_2" for t in semestralidade2)
    assert any(t.id == "ALG101_2_2" for t in semestralidade2)


def test_listar_filtra_turmas_sem_professor(
    repo_turmas: RepositorioTurmas, repo_professores: RepositorioProfessores
):
    t1 = Turma(nome="Cálculo", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    t2 = Turma(nome="Física", codigo_disc="FIS101", numero_turma=1, semestralidade=2)
    t3 = Turma(nome="Álgebra", codigo_disc="ALG101", numero_turma=2, semestralidade=2)

    p = Professor(matricula="p1", nome_completo="Professor 1")
    repo_professores.salvar(p)
    t1.add_professor(p)

    repo_turmas.salvar(t1)
    repo_turmas.salvar(t2)
    repo_turmas.salvar(t3)

    turmas_sem_professor = repo_turmas.listar(com_professor=False)

    assert len(turmas_sem_professor) == 2
    assert any(t.id == "FIS101_1_2" for t in turmas_sem_professor)
    assert any(t.id == "ALG101_2_2" for t in turmas_sem_professor)


def test_listar_filtra_turmas_com_professor(
    repo_turmas: RepositorioTurmas, repo_professores: RepositorioProfessores
):
    t1 = Turma(nome="Cálculo", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    t2 = Turma(nome="Física", codigo_disc="FIS101", numero_turma=1, semestralidade=2)
    t3 = Turma(nome="Álgebra", codigo_disc="ALG101", numero_turma=2, semestralidade=2)

    p = Professor(matricula="p1", nome_completo="Professor 1")
    repo_professores.salvar(p)
    t1.add_professor(p)

    repo_turmas.salvar(t1)
    repo_turmas.salvar(t2)
    repo_turmas.salvar(t3)

    turmas_com_professor = repo_turmas.listar(com_professor=True)

    assert len(turmas_com_professor) == 1
    assert turmas_com_professor[0].id == "MAT101_1_1"


def test_id_salvo_no_banco_corresponde_ao_id_calculado(repo_turmas: RepositorioTurmas):
    t1 = Turma(nome="Cálculo", codigo_disc="MAT101", numero_turma=3, semestralidade=2)
    t2 = Turma(nome="Física", codigo_disc="FIS101", numero_turma=2, semestralidade=1)

    repo_turmas.salvar(t1)
    repo_turmas.salvar(t2)

    t1_encontrada = repo_turmas.buscar_por_id("MAT101_3_2")
    t2_encontrada = repo_turmas.buscar_por_id("FIS101_2_1")

    assert t1_encontrada is not None
    assert t1_encontrada.id == t1.id == "MAT101_3_2"
    assert t2_encontrada is not None
    assert t2_encontrada.id == t2.id == "FIS101_2_1"


def test_buscar_por_id_devolve_copia_independente(repo_turmas: RepositorioTurmas):
    t = Turma(nome="Cálculo", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    repo_turmas.salvar(t)

    primeira = repo_turmas.buscar_por_id("MAT101_1_1")
    assert primeira is not None
    primeira.nome = "Modifica"

    segunda = repo_turmas.buscar_por_id("MAT101_1_1")
    assert segunda is not None
    assert segunda.nome == "Cálculo"
