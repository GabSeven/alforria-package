from alforria import Professor, Turma


def test_id_composto_por_codigo_numero_semestre():
    t = Turma(nome="Matemática", codigo_disc="MAT101", numero_turma=1, semestralidade=1)

    assert t.id == "MAT101_1_1"


def test_id_muda_ao_mudar_numero_turma():
    t = Turma(nome="Matemática", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    t.numero_turma = 2

    assert t.id != "MAT101_1_1"
    assert t.id == "MAT101_2_1"


def test_id_muda_ao_mudar_semestralidade():
    t = Turma(nome="Matemática", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    t.semestralidade = 2

    assert t.id != "MAT101_1_1"
    assert t.id == "MAT101_1_2"


def test_add_professor_vincula_dos_dois_lados():
    t = Turma(nome="Matemática", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    p = Professor(matricula="p1", nome_completo="Professor 1")
    t.add_professor(p)

    assert t.professor is p
    assert p.turmas_a_lecionar == [t]


def test_add_course_vincula_dos_dois_lados():
    t = Turma(nome="Matemática", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    p = Professor(matricula="p1", nome_completo="Professor 1")
    p.add_course(t)

    assert t.professor is p
    assert p.turmas_a_lecionar == [t]


def test_add_professor_idempotente():
    t = Turma(nome="Matemática", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    p = Professor(matricula="p1", nome_completo="Professor 1")
    t.add_professor(p)
    t.add_professor(p)

    assert t.professor is p
    assert p.turmas_a_lecionar == [t]


def test_add_course_idempotente():
    t = Turma(nome="Matemática", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    p = Professor(matricula="p1", nome_completo="Professor 1")
    p.add_course(t)
    p.add_course(t)

    assert t.professor is p
    assert p.turmas_a_lecionar == [t]


def test_remove_professor_desvincula_dos_dois_lados():
    t = Turma(nome="Matemática", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    p = Professor(matricula="p1", nome_completo="Professor 1")
    t.add_professor(p)
    t.remove_professor()

    assert t.professor is None
    assert p.turmas_a_lecionar == []


def test_remove_course_desvincula_dos_dois_lados():
    t = Turma(nome="Matemática", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    p = Professor(matricula="p1", nome_completo="Professor 1")
    t.add_professor(p)
    p.remove_course(t)

    assert t.professor is None
    assert p.turmas_a_lecionar == []


def test_str_usa_matricula_do_professor():
    t = Turma(nome="Matemática", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    p = Professor(matricula="p1", nome_completo="Professor 1")
    t.add_professor(p)

    assert "p1" in str(t)
