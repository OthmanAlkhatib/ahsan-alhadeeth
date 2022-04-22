import psycopg2
import logging

logger = logging.getLogger()

ADD_USER_STATEMENT = """UPDATE count
                                SET users = users + 1 """

INSERT_USERS_STATEMENT = """INSERT INTO count(users)
                                    VALUES(0)"""


class DataSource:
    def __init__(self, database_url):
        self.database_url = database_url

    def get_connection(self):
        return psycopg2.connect(self.database_url, sslmode="allow")

    @staticmethod
    def close_connection(conn):
        if conn is not None:   # finally Statement Below Will Always be Applied, so I Need This Because Sometimes There is an Error in Connection
            conn.close()

    def create_tables(self):
        commands = (
            """
                CREATE TABLE IF NOT EXISTS count (
                    users INT NOT NULL
                )
            """,)

        conn = None
        try:
            conn = self.get_connection()
            cur = conn.cursor()   # Boss That Make Changes and Commands on Database
            for command in commands:   # Because It is Multi Line of Commands
                cur.execute(command)
            cur.close()
            conn.commit()   # Apply Edits

        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(error)
            raise error

        finally:
            self.close_connection(conn)

    def create_users_row(self):
        conn = None
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute(INSERT_USERS_STATEMENT)
            cur.close()
            conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(error)
            raise error

        finally:
            self.close_connection(conn)

    def add_user(self):
        conn = None
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute(ADD_USER_STATEMENT)
            cur.close()
            conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(error)
            raise error

        finally:
            self.close_connection(conn)
