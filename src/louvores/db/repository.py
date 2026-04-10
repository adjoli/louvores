from sqlmodel import select

from louvores.db.models import Coletanea, Hino


def coletanea_por_codigo(session, codigo: str) -> Coletanea | None:
    stmt = select(Coletanea).where(Coletanea.codigo == codigo)
    return session.exec(stmt).one()


def hino_por_numero(session, numero: int, coletanea: str) -> Hino | None:
    stmt = (
        select(Hino)
        .join(Coletanea)
        .where(Hino.numeracao == numero)
        .where(Coletanea.codigo == coletanea)
    )
    return session.exec(stmt).one()


def hinos_por_coletanea(session, coletanea: str) -> list[Hino] | None:
    stmt = select(Hino).join(Coletanea).where(Coletanea.codigo == coletanea)
    return session.exec(stmt).all()
