import pytest

from louvores.core.config import TEMPLATE_DIR
from louvores.db.database import db
from louvores.db.models import Coletanea, Hino


# ----------------------------------------
@pytest.fixture
def session():
    db.init(":memory:")
    db.connect()
    db.create_tables([Coletanea, Hino])
    yield
    db.drop_tables([Coletanea, Hino])
    db.close()


# ----------------------------------------
@pytest.fixture
def coletanea_factory():
    def _create(**kwargs):
        data = {
            "codigo": "XYZ",
            "titulo": "Coletânea PADRÃO",
        }
        data.update(kwargs)
        return Coletanea(**data)

    return _create


# ----------------------------------------
@pytest.fixture
def hino_factory():
    def _create(**kwargs):
        data = {
            "numeracao": 42,
            "titulo": "Hino PADRÃO",
            "letra": "Letra PADRÃO",
            "creditos": "Autor PADRÃO",
        }
        data.update(kwargs)
        return Hino(**data)

    return _create


# ----------------------------------------
@pytest.fixture
def template_path():
    return TEMPLATE_DIR / "atual.pptx"
