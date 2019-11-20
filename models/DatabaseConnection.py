from psycopg2 import connect, OperationalError


def connect_to_database(username, password, hostname, database):
    try:
        # tworzymy nowe połączenie
        db_connection = connect(user=username, password=password, host=hostname, database=database)
    except OperationalError as e:
        print(e)
    else:
        db_connection.autocommit = True
        return db_connection
