import logging
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from louvores.core.config import CSV_PATH, ZIP_DIR
from louvores.core.logging_config import setup_logging
from louvores.db.database import engine, get_session
from louvores.db.models import SQLModel
from louvores.services.import_service import import_from_csv, importar_letras_zip
from louvores.services.revisao_service import aprovar_hino, buscar_hino
from louvores.services.slide_service import gerar_slides_hino
from louvores.services.stats_service import listar_faltantes, obter_stats

setup_logging()
logger = logging.getLogger(__name__)

app = typer.Typer()
console = Console()


# --------------------------------------------
@app.command(short_help="Criar tabelas no Banco de Dados")
def init_db():
    logger.info("Inicializando o banco de dados...")
    SQLModel.metadata.create_all(bind=engine)
    logger.info("Banco de dados inicializado com sucesso.")


# --------------------------------------------
@app.command(short_help="Carregar dados a partir de arquivos .CSV")
def import_csv():
    with get_session() as session:
        import_from_csv(session, CSV_PATH)


# --------------------------------------------
@app.command(short_help="Gera slides para um hino específico")
def gerar(numeracao: int, coletanea: str, template: str = "default"):
    logger.info(f"Gerando slide para hino {numeracao} [{coletanea}] ...")
    with get_session() as session:
        gerar_slides_hino(session, numeracao, coletanea, template)


# --------------------------------------------
@app.command(short_help="Exibe estatísticas de hinos por coletânea")
def stats():
    with get_session() as session:
        resultados = obter_stats(session)

    table = Table(title="Estatísticas de Hinos")

    table.add_column("Coletânea")
    table.add_column("Código")
    table.add_column("Total", justify="right")
    table.add_column("Com Letra", justify="right")
    table.add_column("%", justify="right")

    for item in resultados:
        table.add_row(
            item["titulo"],
            item["codigo"],
            str(item["total"]),
            str(item["com_letra"]),
            f"{item['percentual']:.1f}%",
        )

    console.print(table)


# --------------------------------------------
@app.command(short_help="Lista hinos sem letra cadastrada")
def faltantes(
    coletanea: str = typer.Option(None, help="Filtrar por coletânea"),
):
    with get_session() as session:
        hinos = listar_faltantes(session, coletanea)

    if not hinos:
        console.print("[green]Nenhum hino faltante! 🎉[/green]")
        return

    table = Table(title="🎵 Hinos sem letra")

    table.add_column("Número", justify="right")
    table.add_column("Título")
    table.add_column("Coletânea")

    for h in hinos:
        table.add_row(
            str(h["numero"]),
            h["titulo"],
            h["coletanea"],
        )

    console.print(table)


# --------------------------------------------
@app.command(short_help="Importa letras dos louvores (em arquivos zipados)")
def importar_letras(
    caminho: Path = typer.Option(ZIP_DIR, help="Pasta com arquivos .zip"),
):
    with get_session() as session:
        importar_letras_zip(session, caminho)


# --------------------------------------------
@app.command(short_help="Revisar letra de um hino e marcar como aprovado")
def revisar(numeracao: int, coletanea: str):
    with get_session() as session:
        hino = buscar_hino(session, numeracao, coletanea)

        if not hino.letra:
            logger.warning(f"Hino {numeracao} não possui letra para revisar.")
            console.print("[yellow]Hino não possui letra para revisar.[/yellow]")
            raise typer.Exit(1)

        status_revisao = "[green]Sim[/green]" if hino.revisado else "[red]Não[/red]"

        console.print(
            Panel(
                f"[bold]Título:[/bold] {hino.titulo}\n"
                f"[bold]Número:[/bold] {hino.numeracao}\n"
                f"[bold]Coletânea:[/bold] {hino.coletanea.codigo} — {hino.coletanea.titulo}\n"
                f"[bold]Créditos:[/bold] {hino.creditos or '—'}\n"
                f"[bold]Revisado:[/bold] {status_revisao}\n\n"
                f"[bold]--- Letra ---[/bold]\n{hino.letra}",
                title="Revisão de Hino",
            )
        )

        if typer.confirm("Aprovar conteúdo?"):
            aprovar_hino(session, hino.id)
            logger.info(f"Hino {numeracao} [{coletanea}] marcado como revisado.")
            console.print("[green]Hino aprovado e marcado como revisado![/green]")
        else:
            console.print("[yellow]Operação cancelada.[/yellow]")


# --------------------------------------------


if __name__ == "__main__":
    app()
