from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import DATABASE_URL

from di.dependent import Injectable

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_session():
    with SessionLocal() as session:
        yield session


class DbSession(Injectable, scope="request"):

    def __init__(self):
        self._session = get_session().__next__()

    @property
    def session(self):
        return self._session
