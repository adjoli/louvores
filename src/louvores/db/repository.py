from peewee import fn

from louvores.db.models import Coletanea, Hino


# --------------------------------------------
def coletanea_por_codigo(codigo: str) -> Coletanea | None:
    return Coletanea.get_or_none(Coletanea.codigo == codigo)


# --------------------------------------------
def listar_coletaneas() -> list[Coletanea]:
    return list(Coletanea.select().order_by(Coletanea.id))


# --------------------------------------------
def hino_por_numero(numero: int, codigo_coletanea: str) -> Hino | None:
    return (
        Hino.select()
        .join(Coletanea)
        .where(Hino.numeracao == numero)
        .where(Coletanea.codigo == codigo_coletanea)
        .first()
    )


# --------------------------------------------
def hinos_por_coletanea(codigo_coletanea: str) -> list[Hino]:
    return list(
        Hino.select()
        .join(Coletanea)
        .where(Coletanea.codigo == codigo_coletanea)
        .order_by(Hino.numeracao)
    )


# --------------------------------------------
def listar_hinos() -> list[Hino]:
    return list(Hino.select().order_by(Hino.numeracao))


# --------------------------------------------
def stats_por_coletanea():
    return (
        Coletanea.select(
            Coletanea.codigo,
            Coletanea.titulo,
            fn.COUNT(Hino.id).alias("total"),
            fn.COUNT(Hino.letra).alias("com_letra"),
            fn.SUM(Hino.revisado.cast("INTEGER")).alias("revisados"),
        )
        .join(Hino)
        .group_by(Coletanea.id)
        .order_by(Coletanea.codigo)
        .tuples()
    )


# --------------------------------------------
def hinos_sem_letra(codigo_coletanea: str | None = None) -> list[Hino]:
    query = Hino.select().where(Hino.letra.is_null(True))

    if codigo_coletanea:
        query = query.join(Coletanea).where(Coletanea.codigo == codigo_coletanea)

    query = query.order_by(Hino.coletanea_id, Hino.numeracao)

    return list(query)


# --------------------------------------------
def atualizar_letra_hino(id_hino: int, letra_hino: str) -> None:
    hino = Hino.get_by_id(id_hino)
    hino.letra = letra_hino
    hino.save()


# --------------------------------------------
def atualizar_revisao_hino(id_hino: int) -> None:
    hino = Hino.get_by_id(id_hino)
    hino.revisado = True
    hino.save()
