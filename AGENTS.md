# AGENTS.md — Louvores

## Stack

- **Python ≥3.14** (`.python-version`), **uv** package manager (`uv.lock`).
- **CLI**: Typer app installed as `louvores` script (`[project.scripts]` → `src.louvores.cli.app:app`).
- **DB**: SQLModel + SQLite (`data/hinos.db`). Tests use `sqlite:///:memory:`.
- **PPTX**: python-pptx, templates in `data/templates/` (keys: `default` → `atual.pptx`, `novo` → `novo.pptx`).
- **Testing**: pytest (configured in `.vscode/settings.json`).

## Setup & dev commands

```bash
uv sync              # install all deps (including dev)
uv pip install -e .  # install package in editable mode (makes `louvores` CLI available)
pytest               # run all tests (in-memory SQLite, no external services)
```

Set `PYTHONPATH` to `src/` if running code directly (not via installed CLI):
```
$env:PYTHONPATH = "$env:PYTHONPATH;src"
```

## CLI commands (`louvores <command>`)

| Command | Description |
|---|---|
| `init-db` | Create SQLite tables |
| `import-csv` | Load hymns from `data/data_to_load.csv` (semicolon-delimited) |
| `importar-letras` | Import lyrics from ZIP files in `data/raw/zip/` |
| `gerar <num> <coletanea> [--template]` | Generate PPTX slides for a hymn |
| `stats` | Show hymn count/coverage per collection |
| `faltantes [--coletanea]` | List hymns without lyrics |

## Architecture

```
src/louvores/
  cli/app.py          Typer CLI entry point
  core/config.py      Path constants (DB_PATH, CSV_PATH, OUTPUT_DIR, TEMPLATE_DIR, ZIP_DIR)
  core/logging_config.py  Logs to logs/app.log + console (INFO level)
  db/models.py        Coletanea + Hino (SQLModel tables)
  db/database.py      SQLite engine + get_session()
  db/repository.py    Query functions
  domain/slide_parts.py   ParteHino / Estrofe / Refrao / SequenciaHino dataclasses
  processors/lyrics_parser.py  Splits lyrics into strophes (no indent) vs refrains (indented)
  ppt/ppt_generator.py     Builds Presentation from template + sequenced parts
  ppt/template_registry.py Maps template names to .pptx files
  ppt/layouts.py       SlideLayout.ESTROFE=1, SlideLayout.REFRAO=2
  services/           Business logic: slide_service, import_service, stats_service
```

## Conventions

- **Separator**: CSV uses `;` delimiter (not comma).
- **Refrain detection**: all lines in a block start with space/tab → refrain; otherwise → strophe.
- **Slide numbering**: footer shows `N/total` on shape index 2.
- **Output naming**: `{CODIGO}-{NUM:03d}-{TITULO}.pptx` in `output/slides/`.
- **Import ZIP naming**: `<COLETANEA>-<NUMERO>.txt` (hyphen separator).

## Environment

`.env` contains `DEEPSEEK_API_KEY` and `OPENAI_API_KEY`. Already in `.gitignore` — do not commit.
`logs/app.log` is auto-created by `logging_config.py`. Already in `.gitignore`.
