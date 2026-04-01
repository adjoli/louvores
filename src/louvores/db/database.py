from sqlmodel import Session, create_engine

from louvores.core.config import DB_PATH

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)


def get_session():
    return Session(engine)
