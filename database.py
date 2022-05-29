import sqlite3
from time import time, sleep

class UsersCRUD:
    def __init__(self):
        self.conn = sqlite3.connect('users.db')
        print('Соединение открыто')
        self.conn.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id VARCHAR(16) NOT NULL,
            user_name VARCHAR(32) NOT NULL,
            user_ref VARCHAR(16) NOT NULL,
            sub INT NOT NULL,
            balance INT NOT NULL DEFAULT 0);""")


        self.cursor = self.conn.cursor()

    def __exist_user(self, user_id) -> bool:
        user = self.cursor.execute("""SELECT user_id FROM users WHERE user_id = ?""", (user_id,)).fetchone()
        return bool(user)

    def __create_user(self, user_id, user_name, user_ref = 0, sub_time=0) -> None:
        sub_time += int(time())
        self.cursor.execute("""INSERT INTO users (user_id, user_name, user_ref, sub) VALUES (?,?,?,?)""", (user_id, user_name, user_ref, sub_time))
        self.conn.commit()

    def count_ref(self, user_ref) -> None:
        count = self.cursor.execute("""SELECT COUNT(user_ref) as KOL FROM users WHERE user_ref = ?""", (user_ref,)).fetchone()
        return count[0]

    def update_cash(self, user_id, cash:int) -> None:
        balance_user = self.cursor.execute("""SELECT balance, user_ref FROM users WHERE user_id = ?""", (user_id,)).fetchone()
        user_ref = balance_user[1]
        result = balance_user[0] + cash
        self.cursor.execute("""UPDATE users SET balance = ? where user_id = ?""", (result, user_id))
        balance_userref = self.cursor.execute("""SELECT balance, user_id FROM users WHERE user_id = ?""", (user_ref,)).fetchone()
        result_ref = balance_userref[0] + 10/cash * 100
        self.cursor.execute("""UPDATE users SET balance = ? where user_id = ?""", (result_ref, balance_userref[1]))
        self.conn.commit()
        print('баланс пополнен!')


    def add_new_user(self, user_id, user_name, user_ref = 0, sub_time = 0) -> bool:
        """Добавление нового пользователя если его нет в таблице user

        Если пользователь есть возвращает True
        Если нет то False"""
        if self.__exist_user(user_id):
            return False
        if not (user_ref and self.__exist_user(user_ref)):
            user_ref = 0
        self.__create_user(user_id, user_name, user_ref, sub_time)
        return True

    def close(self):
        print('Соединение закрыто')
        self.conn.close()

#db = UsersCRUD()
#db.add_new_user(9, 'abcd', 152)
#db.close()







