import sqlite3

DEFAULT_DB = "pysteroids.sqlite3"


class Database:
    def __init__(self, db_name=DEFAULT_DB):
        self._db_name = db_name
        self._connection = sqlite3.connect(self._db_name)
        self._cursor = self._connection.cursor()
        self._initialize_tables()

    def _initialize_tables(self):
        self.exec("""
            CREATE TABLE IF NOT EXISTS leaderboard (
                  name TEXT,
                  score INTEGER,
                  bullets INTEGER,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

    def exec(self, query, *args):
        self._cursor.execute(query, args)
        self._connection.commit()

    def fetchall(self, query, *args):
        return self._cursor.execute(query, args).fetchall()

    def close(self):
        self._connection.close()
