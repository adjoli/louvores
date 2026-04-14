from pathlib import Path

from louvores.core.config import TEMPLATE_DIR

TEMPLATES = {
    "default": TEMPLATE_DIR / "atual.pptx",
    "novo": TEMPLATE_DIR / "novo.pptx",
}


def get_template_path(nome) -> Path:
    try:
        return TEMPLATES[nome]
    except KeyError:
        raise ValueError(f"Template '{nome}' não encontrado")
