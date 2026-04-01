from sqlmodel import Session, create_engine

from src.core.config import DB_PATH

engine = create_engine(f"sqlite:///{DB_PATH}", echo=True)


def get_session():
    return Session(engine)
