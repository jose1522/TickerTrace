from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from .base import BaseModel
from .ticker import Ticker

import settings

engine = create_engine(url=settings.DB_URL)
Session = sessionmaker(bind=engine)


def get_session():
    with Session() as session:
        yield session


def migrate():
    BaseModel.metadata.create_all(engine)


__all__ = ["BaseModel", "get_session", "migrate", "Ticker"]
