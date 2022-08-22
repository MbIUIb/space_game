import sqlite3

from config import database, DBAutentication as dba


class Database:
    def __init__(self):
        self.db = sqlite3.connect(database)
        self.cursor = self.db.cursor()
        self.create_table()

    def __del__(self):
        self.close()

    def create_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users(login TEXT, password TEXT, score INTEGER)""")

    def commit(self):
        self.db.commit()

    def close(self):
        self.db.close()

    def get_user_logins(self):
        self.cursor.execute("""SELECT login FROM users""")
        return self.cursor.fetchall()

    def new_user(self, login, password):
        if (login, ) not in self.get_user_logins():
            self.cursor.execute("""INSERT INTO users (login, password) VALUES(?, ?)""", (login, password))
            self.commit()
            return 1
        return 0

    def del_user(self, login):
        self.cursor.execute("""DELETE FROM users WHERE login == ?""", (login, ))
        self.commit()

    def authentication(self, login, password):
        login = (login, )

        user_password = self.cursor.execute("""SELECT password FROM users WHERE login == ?""", login).fetchone()
        if user_password is None:
            return dba.login_error
        if password == user_password[0]:
            return dba.successful
        return dba.pass_error

    def change_password(self, login, new_password):
        self.cursor.execute("""UPDATE users set password = ? WHERE login == ?""", (new_password, login))
        self.commit()

    def get_user_score(self, login):
        return self.cursor.execute("""SELECT score FROM users WHERE login == ?""", (login,)).fetchone()[0]

    def change_score(self, login, score):
        self.cursor.execute("""UPDATE users set score = ? WHERE login == ?""", (score, login))
        self.commit()

    def top_score(self, vol: int = 10) -> list:
        return self.cursor.execute("""SELECT login, score FROM users ORDER BY score DESC""").fetchmany(vol)
