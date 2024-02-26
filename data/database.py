from config import db_name, user, password, host

import pymysql


class My_Database:
    def __init__(self):
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )

    def __del__(self):
        self.connection.close()

    def create_tables(self):

        query = """CREATE TABLE IF NOT EXISTS users(
                    id INT AUTO_INCREMENT PRIMARY KEY ,
                    tg_id int(30) NOT NULL,
                    nickname_tg varchar(50) NOT NULL,
                    role varchar(30),
                    in_chat varchar(30)
                );"""

        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()

    def insert_one_user(self, tg_id, nickname, role):
        query = f"""INSERT INTO users (tg_id, nickname_tg, role)
            SELECT '{tg_id}', '{nickname}', '{role}'
            WHERE NOT EXISTS (
                SELECT 1 FROM users WHERE tg_id = '{tg_id}'
            )"""

        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()

    def get_free_manager(self, tg_id_client):
        query = f"""select * from users where role = 'manager' and in_chat = '' limit 1"""

        with self.connection.cursor() as cursor:
            cursor.execute(query)
        result = cursor.fetchall()
        if result:
            query = f"""update users set in_chat = '{result[0]['tg_id']}' where tg_id = '{tg_id_client}'"""
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                self.connection.commit()
        try:
            return result[0]
        except:
            return []
    def get_info_user(self, tg_id):
        query = f"""select * from users where tg_id = {tg_id}"""

        with self.connection.cursor() as cursor:
            cursor.execute(query)
        result = cursor.fetchall()
        return result[0]

    def leave_chat(self, tg_id):
        query = f"""select * from users where tg_id = {tg_id}"""

        with self.connection.cursor() as cursor:
            cursor.execute(query)
        result = cursor.fetchall()[0]
        query = f"""update users set in_chat = '' where tg_id = '{result['in_chat']}' or tg_id = {tg_id}"""

        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()
        return result

