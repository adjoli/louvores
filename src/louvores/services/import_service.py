import csv
import logging
import zipfile
from pathlib import Path

from louvores.db.models import Coletanea, Hino
from louvores.db.repository import atualizar_letra_hino, hino_por_numero

logger = logging.getLogger(__name__)


# --------------------------------------------
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


# --------------------------------------------
def importar_letras_zip(session, zip_folder: Path):
    arquivos_zip = list(zip_folder.glob("*.zip"))

    total_atualizados = 0
    total_ignorados = 0
    total_nao_encontrados = 0

    for zip_path in arquivos_zip:
        logger.info(f"Processando: {zip_path.name}")

        with zipfile.ZipFile(zip_path, "r") as z:
            for nome_arquivo in z.namelist():
                if not nome_arquivo.endswith(".txt"):
                    continue

                try:
                    coletanea, numero = _parse_nome_arquivo(nome_arquivo)

                    with z.open(nome_arquivo) as f:
                        conteudo = f.read().decode("utf-8").strip()

                    hino = hino_por_numero(session, numero, coletanea)

                    if not hino:
                        logger.warning(f"Hino não encontrado: {coletanea}-{numero}")
                        total_nao_encontrados += 1
                        continue

                    if hino.letra:
                        logger.info(f"Já possui letra: {coletanea}-{numero}")
                        total_ignorados += 1
                        continue

                    atualizar_letra_hino(session, hino.id, conteudo)
                    total_atualizados += 1
                    logger.info(f"Letra do hino {coletanea}-{numero} carregada!")
                except Exception as e:
                    logger.error(f"Erro ao processar {nome_arquivo}: {e}")

    logger.info("Importação concluída!")

    logger.info(f"total_atualizados: {total_atualizados}")
    logger.info(f"total_ignorados: {total_ignorados}")
    logger.info(f"total_nao_encontrados: {total_nao_encontrados}")


def _parse_nome_arquivo(nome: str) -> tuple[str, str]:
    nome = Path(nome).stem

    coletanea, numero = nome.split("-")

    return coletanea, numero


# --------------------------------------------
