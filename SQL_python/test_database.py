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

def test_employee_and_client_saved_to_database(
        db_cursor,
        created_employee,
        created_client
):
    db_cursor.execute(
        """
        SELECT
            id,
            email,
            username,
            is_active,
            is_blocked
        FROM employees
        where id = %s
        """,
        (created_employee["uuid"],)
    )
    employee_db = db_cursor.fetchone()

    assert employee_db is not None
    assert str(employee_db['id']) == created_employee['uuid']
    assert employee_db['email'] == created_employee['email']
    assert employee_db['is_active'] is True
    assert employee_db['is_blocked'] is False

    db_cursor.execute(
        """
        SELECT
            id,
            created_by_employee_id,
            first_name,
            email
        FROM clients
        where id = %s
        """,
        (created_client["id"],)
    )
    client_db = db_cursor.fetchone()

    assert client_db is not None
    assert str(client_db['id']) == created_client['id']
    assert str(client_db['created_by_employee_id']) == created_employee['uuid']
    assert str(client_db['email']) == created_client['email']

    print()
    print(employee_db)
    print(created_employee)

def test_test_3(db_cursor):
    status = 'BLOCKED'
    client_id = '345bkjbn534bjklb'
    query = """
        UPDATE clients SET status = %s WHERE id = %s"""

    db_cursor.execute(
        query,
        (status, client_id)
    )

    print()
    pprint(db_cursor.fetchall())

# def test_test(db_cursor):
#     db_cursor.execute(
#         """
#         SELECT id, first_name, last_name, email, status
#         FROM clients
#         ORDER BY created_at
#         """
#     )
#
#     clients = db_cursor.fetchall()
#     print()
#     for client in clients:
#         print(client['first_name'])
#
# def test_test_2(db_cursor):
#     status = 'ACTIVE'
#
#     query = """
#         SELECT id, first_name, last_name, email, status
#         FROM clients
#         WHERE status = %s"""
#
#     db_cursor.execute(
#         query,
#         (status,)
#     )
#
#     print()
#     pprint(db_cursor.fetchall())