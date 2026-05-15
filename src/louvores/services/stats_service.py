import logging

from louvores.db.repository import hinos_sem_letra, stats_por_coletanea

logger = logging.getLogger(__name__)


# --------------------------------------------
def obter_stats(session):
    resultados = stats_por_coletanea(session)

    stats = []

    for codigo, titulo, total, com_letra, revisados in resultados:
        nao_revisados = com_letra - (revisados or 0)
        percentual = (com_letra / total * 100) if total > 0 else 0

        stats.append(
            {
                "codigo": codigo,
                "titulo": titulo,
                "total": total,
                "com_letra": com_letra,
                "revisados": revisados or 0,
                "nao_revisados": nao_revisados,
                "percentual": percentual,
            }
        )

    logger.info("Estatísticas calculadas!")

    return stats


# --------------------------------------------
def listar_faltantes(session, codigo_coletanea: str | None = None):
    hinos = hinos_sem_letra(session, codigo_coletanea)

    resultado = []

    for h in hinos:
        resultado.append(
            {
                "numero": h.numeracao,
                "titulo": h.titulo,
                "coletanea": h.coletanea.codigo,
            }
        )

    return resultado
