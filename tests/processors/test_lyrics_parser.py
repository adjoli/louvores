from louvores.domain.slide_parts import Estrofe, Refrao
from louvores.processors.lyrics_parser import processar_hino


# --------------------------------------------
def test_parse_hino_com_estrofe_e_refrao():
    texto = """Linha 1
Linha 2

    Refrao 1
    Refrao 2"""

    resultado = processar_hino(texto)

    assert len(resultado.partes) == 2

    assert isinstance(resultado.partes[0], Estrofe)
    assert isinstance(resultado.partes[1], Refrao)

    assert resultado.partes[0].numero == 1
    assert resultado.partes[1].numero == 2


# --------------------------------------------
def test_parse_multiplas_estrofes_e_refrao():
    texto = """A

    B

C"""

    resultado = processar_hino(texto)

    assert len(resultado.partes) == 3

    assert isinstance(resultado.partes[0], Estrofe)
    assert isinstance(resultado.partes[1], Refrao)
    assert isinstance(resultado.partes[2], Estrofe)


# --------------------------------------------
def test_remove_linhas_vazias():
    texto = """A



    B"""

    resultado = processar_hino(texto)

    assert len(resultado.partes) == 2


# --------------------------------------------
def test_detecta_refrao_por_indentacao():
    texto = """   Linha 1
    Linha 2

Linha 3
Linha 4"""

    resultado = processar_hino(texto)

    assert isinstance(resultado.partes[0], Refrao)


# --------------------------------------------
def test_detecta_estrofe_sem_indentacao():
    texto = """Linha 1
Linha 2"""

    resultado = processar_hino(texto)

    assert isinstance(resultado.partes[0], Estrofe)
