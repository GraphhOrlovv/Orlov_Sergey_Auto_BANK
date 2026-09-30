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