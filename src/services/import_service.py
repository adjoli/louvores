import csv
import logging
from pathlib import Path

from src.db.models import Coletanea, Hino
from src.db.repository import coletanea_por_codigo, coletaneas_dict

logger = logging.getLogger(__name__)


RAW_DIR = Path("data/raw")


def import_coletaneas(session):
    logger.info("Importando coletâneas...")
    with open(RAW_DIR / "coletaneas.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")

        for row in reader:
            session.add(Coletanea(codigo=row["codigo"], nome=row["nome"]))
        session.commit()


def import_CC_HCC(session):
    logger.info("Importando CC e HCC...")
    with open(RAW_DIR / "CC_HCC.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")

        coletaneas = coletaneas_dict(session)

        for row in reader:
            session.add(
                Hino(
                    # coletanea=coletaneas.get(row["codigo"]),
                    id_coletanea=coletaneas.get(row["codigo"]).id,
                    numero=row["codigo"],
                    titulo=row["titulo"],
                    creditos=row["creditos"],
                )
            )
        session.commit()
