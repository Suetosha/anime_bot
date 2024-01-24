import psycopg2
from environs import Env
import psycopg2.extras

env = Env()
env.read_env()


def connect():
    connection = psycopg2.connect(
        host=env('HOST'),
        user=env('USER'),
        password=env('PASSWORD'),
        dbname=env('DBNAME'),
        port=env('PORT')
    )
    return connection


def add_to_db(request):
    connection = None
    try:
        connection = connect()

        with connection.cursor() as cursor:

            cursor.execute(request)

        connection.commit()

    except Exception as err:
        print(err)

    finally:
        if connection:
            connection.close()


def get_from_db(request):
    connection = None
    try:
        connection = connect()

        with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:

            cursor.execute(request)
            data = cursor.fetchall()
            result = []

            for row in data:
                result.append(dict(row))

        return result

    except Exception as err:
        pass

    finally:
        if connection:
            connection.close()

