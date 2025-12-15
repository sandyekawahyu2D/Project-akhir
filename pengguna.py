from connection import mycursor, mydb

class Pengguna:

    def __init__(self):
        pass

    def login(self, username, password):
        sql = "SELECT * FROM pengguna WHERE username = %s AND password = %s"
        val = (username, password)
        mycursor.execute(sql, val)
        return mycursor.fetchone()

    def select_data(self):
        sql = "SELECT * FROM pengguna"
        mycursor.execute(sql)
        return mycursor.fetchall()

    def insert_data(self, nama, username, password, role):
        sql = """
        INSERT INTO pengguna (nama, username, password, role)
        VALUES (%s, %s, %s, %s)
        """
        val = (nama, username, password, role)
        mycursor.execute(sql, val)
        mydb.commit()

    def update_data(self, nama, password, role, username, id):
        sql = """
        UPDATE pengguna
        SET nama=%s, password=%s, role=%s, username=%s
        WHERE id=%s
        """
        val = (nama, password, role, username, id)
        mycursor.execute(sql, val)
        mydb.commit()

    def delete_data(self, id):
        sql = "DELETE FROM pengguna WHERE id = %s"
        mycursor.execute(sql, (id,))
        mydb.commit()

    def select_data_by_id(self, id):
        sql = "SELECT id, nama, username, password, role FROM pengguna WHERE id = %s"
        mycursor.execute(sql, (id,))
        return mycursor.fetchone()
