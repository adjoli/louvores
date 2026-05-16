from louvores.db.models import Coletanea, Hino
from louvores.db.repository import (
    coletanea_por_codigo,
    hino_por_numero,
    hinos_por_coletanea,
    listar_coletaneas,
    listar_hinos,
)


# --------------------------------------------
def test_cria_coletanea(session, coletanea_factory):
    coletanea = coletanea_factory(titulo="Coletânea XYZ")

    coletanea.save()

    assert coletanea.id is not None
    assert coletanea.codigo == "XYZ"
    assert coletanea.titulo == "Coletânea XYZ"


# --------------------------------------------
def test_busca_coletanea_por_codigo(session, coletanea_factory):
    coletanea = coletanea_factory()

    coletanea.save()

    resultado = coletanea_por_codigo("XYZ")

    assert resultado.id is not None
    assert resultado.titulo == "Coletânea PADRÃO"


# --------------------------------------------
def test_listar_coletaneas(session, coletanea_factory):
    coletanea = coletanea_factory()

    coletanea.save()

    resultado = listar_coletaneas()
    assert len(resultado) > 0


# --------------------------------------------
def test_cria_hino(session, coletanea_factory, hino_factory):
    hino = hino_factory()
    coletanea = coletanea_factory()

    coletanea.save()
    hino.coletanea = coletanea
    hino.save()

    assert hino.id is not None
    assert hino.titulo == "Hino PADRÃO"


# --------------------------------------------
def test_busca_hino_por_numero(session, coletanea_factory, hino_factory):
    hino = hino_factory(numeracao=42, titulo="Especial")
    coletanea = coletanea_factory()

    coletanea.save()
    hino.coletanea = coletanea
    hino.save()

    resultado = hino_por_numero(42, "XYZ")

    assert resultado.titulo == "Especial"


# --------------------------------------------
def test_busca_hinos_por_coletanea(session, coletanea_factory, hino_factory):
    c1 = coletanea_factory(codigo="ABC")
    c2 = coletanea_factory(codigo="DEF")

    hinos_c1 = [hino_factory(numeracao=1), hino_factory(numeracao=2)]

    hinos_c2 = [
        hino_factory(numeracao=3),
        hino_factory(numeracao=4),
        hino_factory(numeracao=5),
    ]

    c1.save()
    c2.save()

    for h in hinos_c1:
        h.coletanea = c1
        h.save()

    for h in hinos_c2:
        h.coletanea = c2
        h.save()

    assert len(hinos_por_coletanea("ABC")) == 2
    assert len(hinos_por_coletanea("DEF")) == 3

    # Aproveitando os hinos criados para testar a função "listar_hinos()"
    assert len(listar_hinos()) == 5  # total de hinos criados
