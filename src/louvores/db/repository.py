from sqlmodel import select

from louvores.db.models import Coletanea, Hino


def hino_por_numero(session, numero: int, coletanea: str) -> Hino | None:
    return session.exec(
        select(Hino)
        .join(Coletanea)
        .where(Hino.numeracao == numero)
        .where(Coletanea.codigo == coletanea)
    ).one()
