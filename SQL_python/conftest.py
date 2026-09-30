import pytest
import psycopg
from psycopg.rows import dict_row

from sshtunnel import SSHTunnelForwarder

from credentials import (
    SSH_HOST,
    SSH_PORT,
    SSH_USER,
    SSH_PASSWORD,
    REMOTE_POSTGRES_HOST,
    REMOTE_POSTGRES_PORT,
    LOCAL_BIND_ADDRESS,
    LOCAL_BIND_PORT,
    POSTGRES_DB,
    POSTGRES_USER,
    POSTGRES_PASSWORD
)


@pytest.fixture(scope='session')
def ssh_tunnel():
    tunnel = SSHTunnelForwarder(
        (SSH_HOST, SSH_PORT),
        ssh_username=SSH_USER,
        ssh_password=SSH_PASSWORD,
        remote_bind_adress=(
            REMOTE_POSTGRES_HOST,
            REMOTE_POSTGRES_PORT
        ),
        local_bind_adress=(
            LOCAL_BIND_ADDRESS,
            LOCAL_BIND_PORT
        )
    )
    tunnel.start()
    yield tunnel
    tunnel.stop()

@pytest.fixture
def db_connection(ssh_tunnel): # Наш коннект к БД
    connection = psycopg.connect(
        host=REMOTE_POSTGRES_HOST,
        port=ssh_tunnel.local_bind_port,
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        connect_timeout=10,
        application_name='aqa_pytest',
        options='-c statement_timeout=10000',
        row_factory=dict_row
    )
    yield connection
    connection.close()

@pytest.fixture
def db_cursor(db_connection): # Это уже для запросов
    cursor = db_connection.cursor()
    yield cursor
    cursor.close()