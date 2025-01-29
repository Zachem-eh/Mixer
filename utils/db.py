import logging
import sqlite3
import time
from datetime import datetime

# логгер для вывода ошибок
log = logging.getLogger(__name__)

PATH = "base.db"


class User:
    """
    класс пользователя в бд

    Attributes:
        username: логин пользователя
        reg_date: дата регистрации
        curr_lvl: текущий уровень
    """
    username: str
    reg_date: str
    curr_lvl: int

    def __init__(self, *args):
        if len(args) == 3:
            (self.username, self.reg_date, self.curr_lvl), self.start_time = args, None
        else:
            self.username, self.reg_date, self.curr_lvl, self.start_time = args
        self.start_time = float(self.start_time) if self.start_time else None


class Database:
    def __init__(self):
        self.db_name = "users"
        self._create_table()

    def connect(self):
        return sqlite3.connect(PATH)

    def _sql(self, query, args=(), executemany=False):
        """
        функция выполняет SQL запрос
        """
        try:
            conn = self.connect()
            query = query.format(self.db_name)
            c = conn.cursor()

            if not executemany:
                c.execute(query, args)
            else:
                c.executemany(query, args)

            if query.strip().upper().startswith('SELECT'):
                result = c.fetchall()
            elif query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')):
                conn.commit()
                result = c.rowcount
            else:
                conn.commit()
                result = c.fetchall()
            return result
        except sqlite3.Error as e:
            log.error(f"Ошибка при SQL запросе: {e}. Query: {query}. Args: {args}")
            return None
        finally:
            if conn:
                conn.close()

    def __call__(self, *args, **kwargs):
        return self._sql(*args, **kwargs)

    def _create_table(self):
        return self(
            f'CREATE TABLE IF NOT EXISTS {self.db_name} ('
            f'username TEXT NOT NULL PRIMARY KEY,'
            f'reg_date TEXT NOT NULL,'  # дата регистрации
            f'curr_lvl INTEGER NOT NULL DEFAULT 1,'
            f'start_time TEXT DEFAULT NULL'  # текущий уровень. По умолчанию первый
            f')'
        )

    def get_user(self, username: str) -> User | None:
        response = self("SELECT * FROM {} WHERE username = ?", (username,))
        return User(*response[0]) if response else None

    def update_user(self, username, **kwargs):
        if "start_time" in kwargs:
            kwargs["start_time"] = str(kwargs["start_time"])
        args_query = ', '.join([f"{key} = ?" for key in kwargs.keys()])
        query = f"UPDATE {self.db_name} SET {args_query} WHERE username = ?"
        return self(query, (*tuple(kwargs.values()), username))

    def new_user(self, username: str) -> User:
        already_user = self.get_user(username)
        if not already_user:
            reg_date = datetime.now().isoformat()
            self(F"INSERT INTO {self.db_name} (username, reg_date) VALUES (?, ?)", (username, reg_date))
            return User(username, reg_date, 1)
        else:
            return already_user

    def next_lvl(self, username) -> int:
        user = self.get_user(username)
        self.update_user(username, start_time=time.time())
        if user.curr_lvl == 4:
            return user.curr_lvl
        user.curr_lvl += 1
        self.update_user(username, curr_lvl=user.curr_lvl)
        return user.curr_lvl


db = Database()
