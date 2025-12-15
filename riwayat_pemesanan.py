from connection import mycursor


class RiwayatPemesanan:
    def select_all(self):
        sql = """
        SELECT
            p.id_pemesanan,
            u.username,
            t.nama,
            p.jumlah_tiket,
            p.total_harga,
            p.tanggal_pesan
        FROM pemesanan p
        JOIN pengguna u ON p.id_pengguna = u.id
        JOIN tiket t ON p.id_tiket = t.id_tiket
        ORDER BY p.tanggal_pesan DESC
        """
        mycursor.execute(sql)
        return mycursor.fetchall()
