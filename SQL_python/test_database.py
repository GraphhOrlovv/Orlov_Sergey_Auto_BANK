from pprint import pprint

from credentials import POSTGRES_DB, POSTGRES_USER


def test_database_connection(db_cursor):
    db_cursor.execute(
        """
        SELECT
            current_database() AS database_name,
            current_user AS database_user,
            current_schema() AS schema_name
        """
    )

    database_info = db_cursor.fetchone()

    assert database_info is not None
    assert database_info['database_name'] == POSTGRES_DB
    assert database_info['database_user'] == POSTGRES_USER

    print(database_info)

def test_test(db_cursor):
    db_cursor.execute(
        """
        SELECT id, first_name, last_name, email, status
        FROM clients
        ORDER BY created_at
        """
    )

    clients = db_cursor.fetchall()
    print()
    for client in clients:
        print(client['first_name'])

def test_test_2(db_cursor):
    status = 'ACTIVE'

    query = f"""
        SELECT id, first_name, last_name, email, status
        FROM clients
        WHERE status = %s"""

    db_cursor.execute(
        query,
        (status,)
    )

    print()
    pprint(db_cursor.fetchall())