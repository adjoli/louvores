from louvores.db.models import Coletanea, Hino
from louvores.db.repository import (
    coletanea_por_codigo,
    hino_por_numero,
    hinos_por_coletanea,
)


# --------------------------------------------
def test_cria_coletanea(session, coletanea_factory):
    coletanea = coletanea_factory(titulo="Coletânea XYZ")

    session.add(coletanea)
    session.commit()

    assert coletanea.id is not None
    assert coletanea.codigo == "XYZ"
    assert coletanea.titulo == "Coletânea XYZ"


# --------------------------------------------
def test_busca_coletanea_por_codigo(session, coletanea_factory):
    coletanea = coletanea_factory()

    session.add(coletanea)
    session.commit()

    resultado = coletanea_por_codigo(session, "XYZ")


# --------------------------------------------
def test_cria_hino(session, coletanea_factory, hino_factory):
    hino = hino_factory()
    hino.coletanea = coletanea_factory()

    session.add(hino)
    session.commit()

    assert hino.id is not None
    assert hino.titulo == "Hino PADRÃO"


# --------------------------------------------
def test_busca_hino_por_numero(session, coletanea_factory, hino_factory):
    hino = hino_factory(numeracao=42, titulo="Especial")
    hino.coletanea = coletanea_factory()

    session.add(hino)
    session.commit()

    resultado = hino_por_numero(session, 42, "XYZ")

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

    c1.hinos.extend(hinos_c1)
    c2.hinos.extend(hinos_c2)

    session.add_all([c1, c2])
    session.commit()

    assert len(hinos_por_coletanea(session, "ABC")) == 2
    assert len(hinos_por_coletanea(session, "DEF")) == 3
