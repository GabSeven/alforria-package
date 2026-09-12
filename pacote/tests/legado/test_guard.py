import re
from pathlib import Path


def test_nenhuma_chamada_id_como_metodo_no_src():
    raiz = Path(__file__).resolve().parents[2] / "src" / "alforria"
    padrao = re.compile(r"\.id\(")
    arquivos_ruins = []
    for arquivo in raiz.rglob("*.py"):
        if padrao.search(arquivo.read_text(encoding="utf-8")):
            arquivos_ruins.append(str(arquivo))
    assert arquivos_ruins == []


def test_imports_legado_carregam():
    import alforria.check
    import alforria.cli
    import alforria.funcoes_escrita
    import alforria.funcoes_leitura
