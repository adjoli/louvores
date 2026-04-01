from sqlmodel import select

from src.db.models import Coletanea, Hino


def hino_por_numero(session, numero: int, coletanea: str) -> Hino | None:
    return session.exec(
        select(Hino)
        .join(Coletanea)
        .where(Hino.numero == numero)
        .where(Coletanea.codigo == coletanea)
    ).one()


def coletanea_por_codigo(session, codigo) -> Coletanea | None:
    return session.exec(select(Coletanea).where(Coletanea.codigo == codigo)).one()


def coletaneas_dict(session):
    coletaneas = session.exec(select(Coletanea)).all()
    return {c.codigo: c for c in coletaneas}
