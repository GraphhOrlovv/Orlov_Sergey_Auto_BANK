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
    POSTGRES_PASSWORD,
    STUDENT_LOGIN,
    STUDENT_PASSWORD,
    EMPLOYEE_EMAIL,
    EMPLOYEE_PASSWORD
)

from api_client import (
    login,
    create_employee,
    delete_employee,
    create_client,
    delete_client
)
from faker import Faker
fake = Faker()

@pytest.fixture(scope='session')
def ssh_tunnel():
    tunnel = SSHTunnelForwarder(
        (SSH_HOST, SSH_PORT),
        ssh_username=SSH_USER,
        ssh_password=SSH_PASSWORD,
        remote_bind_address=(
            REMOTE_POSTGRES_HOST,
            REMOTE_POSTGRES_PORT
        ),
        local_bind_address=(
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

@pytest.fixture(scope="session")
def student_token():
    return login(STUDENT_LOGIN, STUDENT_PASSWORD, "CLIENT")

@pytest.fixture
def created_employee(student_token):
    employee = create_employee(
        student_token,
        EMPLOYEE_EMAIL,
        EMPLOYEE_PASSWORD
    )

    yield employee

    delete_employee(student_token, employee["id"])

@pytest.fixture
def created_client(
        student_token,
        created_employee
):
    client_email = fake.email()
    client_data = {
          "student_username": client_email,
          "first_name": fake.name(),
          "last_name": fake.last_name(),
          # "birth_date": str(fake.date_between(
          #     start_date="-60y",
          #     end_date="-20y"
          # )),
          "phone": fake.phone_number(),
          "email": client_email
}
    client = create_client(
        student_token,
        created_employee["id"],
        client_data
    )

    yield client

    delete_client(student_token, client["id"])