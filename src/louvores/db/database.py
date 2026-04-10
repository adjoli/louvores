from contextlib import contextmanager

from sqlmodel import Session, create_engine

from louvores.core.config import DB_PATH

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)


@contextmanager
def get_session():
    with Session(engine) as session:
        yield session
