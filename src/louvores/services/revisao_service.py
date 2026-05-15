import logging

from louvores.db.models import Hino
from louvores.db.repository import (
    atualizar_revisao_hino,
    hino_por_numero,
)

logger = logging.getLogger(__name__)


def buscar_hino(session, num_hino: int, coletanea: str) -> Hino:
    hino = hino_por_numero(session, num_hino, coletanea)
    if hino is None:
        raise ValueError(f"Hino {num_hino} não encontrado na coletânea '{coletanea}'")
    return hino


def aprovar_hino(session, id_hino: int) -> None:
    atualizar_revisao_hino(session, id_hino)
    logger.info(f"Hino {id_hino} marcado como revisado!")
