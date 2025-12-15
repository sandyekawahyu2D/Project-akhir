from connection import mycursor, mydb

class Tiket:
    def __init__(self, id_tiket=None, nama=None, harga_dasar=None, stok=None):
        self.id_tiket = id_tiket
        self.nama = nama
        self.harga_dasar = harga_dasar
        self.stok = stok

    def select_data(self):
        sql = "SELECT id_tiket, nama, harga_dasar, stok FROM tiket"
        mycursor.execute(sql)
        return mycursor.fetchall()

    def select_data_by_id(self, id_tiket):
        sql = """
        SELECT id_tiket, nama, harga_dasar, stok
        FROM tiket
        WHERE id_tiket = %s
        """
        mycursor.execute(sql, (id_tiket,))
        return mycursor.fetchone()

    def update_stok(self, id_tiket, jumlah):
        sql = """
        UPDATE tiket
        SET stok = stok - %s
        WHERE id_tiket = %s
        """
        mycursor.execute(sql, (jumlah, id_tiket))
        mydb.commit()
