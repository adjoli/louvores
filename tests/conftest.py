import pytest
from sqlmodel import Session, SQLModel, create_engine

from louvores.core.config import TEMPLATE_DIR
from louvores.db.models import Coletanea, Hino


# ----------------------------------------
@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


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
