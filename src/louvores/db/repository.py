from sqlmodel import func, select

from louvores.db.models import Coletanea, Hino


# --------------------------------------------
def coletanea_por_codigo(session, codigo: str) -> Coletanea | None:
    stmt = select(Coletanea).where(Coletanea.codigo == codigo)
    return session.exec(stmt).one_or_none()


# --------------------------------------------
def listar_coletaneas(session) -> list[Coletanea]:
    stmt = select(Coletanea).order_by(Coletanea.id)
    return session.exec(stmt).all()


# --------------------------------------------
def hino_por_numero(session, numero: int, coletanea: str) -> Hino | None:
    stmt = (
        select(Hino)
        .join(Coletanea)
        .where(Hino.numeracao == numero)
        .where(Coletanea.codigo == coletanea)
    )
    return session.exec(stmt).one_or_none()


# --------------------------------------------
def hinos_por_coletanea(session, codigo_coletanea: str) -> list[Hino]:
    stmt = (
        select(Hino)
        .join(Coletanea)
        .where(Coletanea.codigo == codigo_coletanea)
        .order_by(Hino.numeracao)
    )
    return session.exec(stmt).all()


# --------------------------------------------
def listar_hinos(session) -> list[Hino]:
    stmt = select(Hino).order_by(Hino.numeracao)
    return session.exec(stmt).all()


# --------------------------------------------
def stats_por_coletanea(session):
    stmt = (
        select(
            Coletanea.codigo,
            Coletanea.titulo,
            func.count(Hino.id).label("total"),
            func.count(Hino.letra).label("com_letra"),  # Conta apenas linhas NOT NULL
        )
        .join(Hino)
        .group_by(Coletanea.id)
        .order_by(Coletanea.codigo)
    )

    return session.exec(stmt)


# --------------------------------------------
def hinos_sem_letra(session, codigo_coletanea: str | None = None) -> list[Hino]:
    stmt = select(Hino).where(Hino.letra.is_(None))

    if codigo_coletanea:
        stmt = stmt.join(Coletanea).where(Coletanea.codigo == codigo_coletanea)

    stmt = stmt.order_by(Hino.numeracao)

    return session.exec(stmt).all()


# --------------------------------------------
def atualizar_letra_hino(session, id_hino: int, letra_hino: str) -> None:
    hino = session.get(Hino, id_hino)
    hino.letra = letra_hino
    session.commit()
