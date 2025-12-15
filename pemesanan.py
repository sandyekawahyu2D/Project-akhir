from connection import mycursor, mydb

class Pemesanan:

    def __init__(self):
        pass

    def insert_data(self, id_pengguna, id_tiket, jumlah_tiket, total_harga):
        sql = """
        INSERT INTO pemesanan
        (id_pengguna, id_tiket, tanggal_pesan, jumlah_tiket, total_harga)
        VALUES (%s, %s, CURDATE(), %s, %s)
        """
        val = (id_pengguna, id_tiket, jumlah_tiket, total_harga)
        mycursor.execute(sql, val)
        mydb.commit()

    def select_data(self):
        sql = """
        SELECT p.id_pemesanan, g.nama, t.nama,
               p.tanggal_pesan, p.jumlah_tiket, p.total_harga
        FROM pemesanan p
        JOIN pengguna g ON p.id_pengguna = g.id
        JOIN tiket t ON p.id_tiket = t.id_tiket
        """
        mycursor.execute(sql)
        return mycursor.fetchall()

    def delete_data(self, id_pemesanan):
        sql = "DELETE FROM pemesanan WHERE id_pemesanan = %s"
        mycursor.execute(sql, (id_pemesanan,))
        mydb.commit()
