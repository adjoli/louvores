import csv
import logging
from pathlib import Path

from louvores.db.models import Coletanea, Hino

logger = logging.getLogger(__name__)


def import_from_csv(session, path: Path):
    logger.info(f"Importando dados de {path}")

    coletaneas: dict[str, Coletanea] = {}

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")

        for i, row in enumerate(reader, start=1):
            try:
                titulo_coletanea = row["coletanea"]
                codigo_coletanea = row["codigo"]

                dados_hino = {
                    k: v for k, v in row.items() if k not in ("coletanea", "codigo")
                }

                hino = Hino(**dados_hino)

                if codigo_coletanea not in coletaneas:
                    coletanea = Coletanea(
                        codigo=codigo_coletanea, titulo=titulo_coletanea
                    )
                    session.add(coletanea)
                    coletaneas[codigo_coletanea] = coletanea

                coletaneas[codigo_coletanea].hinos.append(hino)
            except Exception as e:
                logger.error(f"Erro na linha {i}: {e}")

            session.commit()

    logger.info("Importação concluída!")
