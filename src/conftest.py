import pytest

from .core.db import Base, engine


@pytest.fixture(autouse=True)
def load_db_inmem(monkeypatch):
    """
    Load the database in memory
    """
    Base.metadata.create_all(engine)
