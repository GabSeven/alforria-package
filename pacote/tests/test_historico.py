from alforria.historico import HistoricoAlteracoes, RegistroOperacao, TipoOperacao


def test_historico_comeca_vazio():
    historico = HistoricoAlteracoes()

    assert not historico.pode_desfazer()
    assert not historico.pode_refazer()
    assert historico.desfazer() is None
    assert historico.refazer() is None


def test_registrar_operacao_permite_desfazer():
    historico = HistoricoAlteracoes()

    reg1 = RegistroOperacao(TipoOperacao.ATRIBUIR, "MAT101_1_1", "p1")
    historico.registrar(reg1)

    reg2 = RegistroOperacao(TipoOperacao.MOVER, "MAT101_1_1", "p2", "p1")
    historico.registrar(reg2)

    assert historico.pode_desfazer()
    assert historico.desfazer() is reg2
    assert historico.pode_desfazer()
    assert historico.desfazer() is reg1


def test_desfazer_move_para_pilha_de_refazer():
    historico = HistoricoAlteracoes()

    reg = RegistroOperacao(TipoOperacao.ATRIBUIR, "MAT101_1_1", "p1")
    historico.registrar(reg)
    historico.desfazer()

    assert historico.pode_refazer()
    assert not historico.pode_desfazer()
    assert historico.desfazer() is None
    assert historico.refazer() is reg


def test_refazer_retorna_registro_desfeito():
    historico = HistoricoAlteracoes()

    reg = RegistroOperacao(TipoOperacao.ATRIBUIR, "MAT101_1_1", "p1")
    historico.registrar(reg)
    historico.desfazer()
    historico.refazer()

    assert historico.pode_desfazer()
    assert not historico.pode_refazer()
    assert historico.refazer() is None
    assert historico.desfazer() is reg


def test_registrar_apos_desfazer_limpa_refazer():
    historico = HistoricoAlteracoes()

    reg1 = RegistroOperacao(TipoOperacao.ATRIBUIR, "MAT101_1_1", "p1")
    historico.registrar(reg1)
    historico.desfazer()

    reg2 = RegistroOperacao(TipoOperacao.ATRIBUIR, "MAT101_1_1", "p2")
    historico.registrar(reg2)

    assert not historico.pode_refazer()
    assert historico.refazer() is None
