import csv
import logging
from pathlib import Path
from typing import Dict

from louvores.db.models import Coletanea, Hino

logger = logging.getLogger(__name__)


RAW_DIR = Path("data/raw")


def import_data(session):
    logger.info("Importando dados...")
    with open(RAW_DIR / "data_to_load.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")

        coletaneas: Dict[str, Coletanea] = {}
        for row in reader:
            titulo_coletanea = row.pop("coletanea")
            codigo_coletanea = row.pop("codigo")

            hino = Hino(**row)
            if codigo_coletanea not in coletaneas:
                coletanea = Coletanea(codigo=codigo_coletanea, titulo=titulo_coletanea)
                session.add(coletanea)
                coletaneas[codigo_coletanea] = coletanea
            coletaneas[codigo_coletanea].hinos.append(hino)
        session.commit()
    logger.info("Importação concluída!")
