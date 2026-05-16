import logging

from louvores.core.config import OUTPUT_DIR
from louvores.db.repository import hino_por_numero
from louvores.ppt.ppt_generator import create_slides
from louvores.ppt.template_registry import get_template_path
from louvores.processors.lyrics_parser import processar_hino

logger = logging.getLogger(__name__)


def gerar_slides_hino(num_hino: int, coletanea: str, template: str):
    hino = hino_por_numero(num_hino, coletanea)

    if hino is None:
        raise ValueError(f"Hino {num_hino} não encontrado")

    template_path = get_template_path(template)

    sequencia = processar_hino(hino.letra)
    prs = create_slides(hino, sequencia, template_path)

    nome_hino = (
        f"{hino.coletanea.codigo}-{hino.numeracao:03}-{hino.titulo.upper()}.pptx"
    )
    prs.save(OUTPUT_DIR / nome_hino)

    logger.info(f"{nome_hino} criado em {OUTPUT_DIR}")
