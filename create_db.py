import psycopg2
import config

connection = None

try:
    connection = psycopg2.connect(
        host=config.HOST,
        user=config.USER,
        password=config.PASSWORD,
        dbname=config.DBNAME,
        port=config.PORT
    )
    print(connection)

    with connection.cursor() as cursor:

        cursor.execute("""
            DROP TABLE IF EXISTS users CASCADE;

            CREATE TABLE users (
                user_id SERIAL PRIMARY KEY
            );
            
            DROP TABLE IF EXISTS dubbing;
            
            CREATE TABLE dubbing (
                dubbing_id SERIAL PRIMARY KEY,
                studio VARCHAR(50) NOT NULL
            );
            
            DROP TABLE IF EXISTS anime;
            
            CREATE TABLE anime (
                anime_id SERIAL PRIMARY KEY,
                title VARCHAR(50) NOT NULL
            );
            
            DROP TABLE IF EXISTS subscription;
            
            CREATE TABLE subscription (
                subscription_id SERIAL PRIMARY KEY,
                user_id INT,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                dubbing_id INT,
                FOREIGN KEY (dubbing_id) REFERENCES dubbing (dubbing_id),
                anime_id INT,
                FOREIGN KEY (anime_id) REFERENCES anime (anime_id)
            );
            """)

    connection.commit()

except Exception as err:
    print(err)

finally:
    if connection:
        connection.close()