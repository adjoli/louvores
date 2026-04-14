import logging

from louvores.db.repository import stats_por_coletanea

logger = logging.getLogger(__name__)


def obter_stats(session):
    resultados = stats_por_coletanea(session)

    stats = []

    for codigo, titulo, total, com_letra in resultados:
        percentual = (com_letra / total * 100) if total > 0 else 0

        stats.append(
            {
                "codigo": codigo,
                "titulo": titulo,
                "total": total,
                "com_letra": com_letra,
                "percentual": percentual,
            }
        )

    logger.info("Estatísticas calculadas!")

    return stats
