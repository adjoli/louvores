import logging

import typer

from louvores.core.config import CSV_PATH, TEMPLATE_DIR
from louvores.core.logging_config import setup_logging
from louvores.db.database import engine, get_session
from louvores.db.models import SQLModel
from louvores.services.import_service import import_from_csv
from louvores.services.slide_service import gerar_slides_hino

setup_logging()
logger = logging.getLogger(__name__)

app = typer.Typer()


@app.command(short_help="Criar tabelas no Banco de Dados")
def init_db():
    logger.info("Inicializando o banco de dados...")
    SQLModel.metadata.create_all(bind=engine)
    logger.info("Banco de dados inicializado com sucesso.")


@app.command(short_help="Carregar dados a partir de arquivos .CSV")
def import_csv():
    with get_session() as session:
        import_from_csv(session, CSV_PATH)


@app.command(short_help="Gera slides para um hino específico")
def gerar(numeracao: int, coletanea: str, template: str = "default"):
    logger.info(f"Gerando slide para hino {numeracao} [{coletanea}] ...")
    with get_session() as session:
        gerar_slides_hino(session, numeracao, coletanea, template)


if __name__ == "__main__":
    app()

# Exportar variável de ambiente
# $env:PYTHONPATH = "$env:PYTHONPATH;C:\Users\N2SE\OneDrive - TRANSPETRO\Documentos\Projetos\louvores\src"

# uv pip install -e .
