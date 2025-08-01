import typing

import pytest
import sqlalchemy
from testcontainers import postgres


@pytest.fixture(scope="session")
def pg_container() -> typing.Generator[sqlalchemy.engine.Engine, None, None]:
    with postgres.PostgresContainer("postgres:15") as pg:
        engine = sqlalchemy.create_engine(pg.get_connection_url())
        yield engine
        engine.dispose()
