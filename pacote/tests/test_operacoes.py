from alforria import Professor, Turma
from alforria.excecoes import TurmaJaAtribuidaError, TurmaSemProfessorError
from alforria.operacoes import atribuir_turma, mover_turma, remover_turma
from pytest import raises


def test_atribuir_turma_sincroniza_os_dois_lados():
    p = Professor(matricula="p1", nome_completo="Professor 1")
    t = Turma(nome="Matemática", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    atribuir_turma(t, p)

    assert len(p.turmas_a_lecionar) == 1
    assert p.turmas_a_lecionar[0] is t
    assert t.professor is p


def test_atribuir_mesmo_professor_nao_duplica():
    p = Professor(matricula="p1", nome_completo="Professor 1")
    t = Turma(nome="Matemática", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    atribuir_turma(t, p)
    atribuir_turma(t, p)

    assert len(p.turmas_a_lecionar) == 1


def test_atribuir_turma_com_outro_dono_levanta_erro():
    p1 = Professor(matricula="p1", nome_completo="Professor 1")
    p2 = Professor(matricula="p2", nome_completo="Professor 2")
    t = Turma(nome="Matemática", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    atribuir_turma(t, p1)

    with raises(TurmaJaAtribuidaError):
        atribuir_turma(t, p2)


def test_remover_turma_limpa_os_dois_lados():
    p = Professor(matricula="p1", nome_completo="Professor 1")
    t = Turma(nome="Matemática", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    atribuir_turma(t, p)
    remover_turma(t)

    assert p.turmas_a_lecionar == []
    assert t.professor is None


def test_remover_turma_sem_professor_e_noop():
    t = Turma(nome="Matemática", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    remover_turma(t)


def test_mover_turma_entre_professores():
    p1 = Professor(matricula="p1", nome_completo="Professor 1")
    p2 = Professor(matricula="p2", nome_completo="Professor 2")
    t = Turma(nome="Matemática", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    atribuir_turma(t, p1)

    mover_turma(t, p2)

    assert p1.turmas_a_lecionar == []
    assert len(p2.turmas_a_lecionar) == 1
    assert p2.turmas_a_lecionar[0] is t
    assert t.professor is p2


def test_mover_turma_sem_dono_levanta_erro():
    p = Professor(matricula="p1", nome_completo="Professor 1")
    t = Turma(nome="Matemática", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    with raises(TurmaSemProfessorError):
        mover_turma(t, p)


def test_mover_para_o_mesmo_professor_e_noop():
    p = Professor(matricula="p1", nome_completo="Professor 1")
    t = Turma(nome="Matemática", codigo_disc="MAT101", numero_turma=1, semestralidade=1)
    atribuir_turma(t, p)
    mover_turma(t, p)

    assert len(p.turmas_a_lecionar) == 1
    assert t.professor is p
