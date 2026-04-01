from sqlmodel import SQLModel

from louvores.db.database import engine
from louvores.db.models import Coletanea, Hino


def main():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    main()


# Execução
# uv run python -m scripts.init_db
