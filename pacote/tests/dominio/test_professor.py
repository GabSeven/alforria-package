from alforria import Professor, Turma


def test_matricula_eh_indentificador_direto():
    p = Professor(matricula="p1", nome_completo="Professor 1")

    assert p.matricula == "p1"


def test_nao_existe_property_id():
    p = Professor(matricula="p1", nome_completo="Professor 1")

    assert not hasattr(p, "id")


def test_mesma_matricula_sao_iguais():
    p1 = Professor(matricula="p1", nome_completo="teste 1")
    p2 = Professor(matricula="p1", nome_completo="teste 2")

    assert p1 == p2


def test_mesma_matricula_mesmo_hash():
    p1 = Professor(matricula="p1", nome_completo="teste 1")
    p2 = Professor(matricula="p1", nome_completo="teste 2")

    assert hash(p1) == hash(p2)


def test_mesma_matricula_unica_em_set():
    p1 = Professor(matricula="p1", nome_completo="teste 1")
    p2 = Professor(matricula="p1", nome_completo="teste 2")

    assert len({p1, p2}) == 1


def test_matriculas_diferentes_diferentes():
    p1 = Professor(matricula="p1", nome_completo="teste 1")
    p3 = Professor(matricula="p3", nome_completo="teste 1")

    assert p1 != p3


def test_nome_com_underscores():
    p = Professor(matricula="p1", nome_completo="Gabriel Rodrigues Gomes")

    assert p.nome() == "Gabriel_Rodrigues_Gomes"


def test_display_comeca_com_nome():
    p = Professor(matricula="p1", nome_completo="Professor 1")

    assert p.display().startswith(p.nome())


def test_display_sem_pos_nao_mostra_marcador():
    p = Professor(matricula="p1", nome_completo="Professor 1")
    p.pos = False

    assert " P " not in p.display()


def test_display_marca_pos():
    p = Professor(matricula="p1", nome_completo="Professor 1")
    p.pos = True

    assert " P " in p.display()


def test_display_mostra_cargas_previas():
    p = Professor(matricula="p1", nome_completo="Professor 1")
    p.chprevia1 = 4.0
    p.chprevia2 = 6.0

    assert "Ch. previa: 4 (1S) 6 (2S)" in p.display()


def test_display_mostra_cargas_atuais_s1_s2():
    p = Professor(matricula="p1", nome_completo="Professor 1")
    t1 = Turma(nome="Cálculo", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    t2 = Turma(nome="Física", codigo_disc="FIS101", numero_turma=1, semestralidade=2)
    t1.ch = 4
    t2.ch = 3
    p.add_course(t1)
    p.add_course(t2)

    assert "Ch. total: 4 (1S) 3 (2S)" in p.display()


def test_display_lista_turmas_a_lecionar():
    p = Professor(matricula="p1", nome_completo="Professor 1")
    t1 = Turma(nome="Cálculo", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    t2 = Turma(nome="Física", codigo_disc="FIS101", numero_turma=1, semestralidade=2)
    t3 = Turma(nome="Álgebra", codigo_disc="ALG101", numero_turma=1, semestralidade=1)

    p.add_course(t1)
    p.add_course(t2)

    assert str(t1) in p.display()
    assert str(t2) in p.display()
    assert str(t3) not in p.display()
