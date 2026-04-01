import os
from contextlib import contextmanager

from dotenv import load_dotenv
from sqlmodel import Session, create_engine

load_dotenv()

engine = create_engine(os.environ["DATABASE_URL"], echo=False)


@contextmanager
def get_session():
    session = Session(engine)
    yield session
    session.close()
