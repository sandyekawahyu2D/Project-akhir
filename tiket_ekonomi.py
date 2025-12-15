from connection import mycursor, mydb
from tiket import Tiket


class TiketEkonomi(Tiket):
    """Kelas TiketEkonomi mewarisi dari Tiket dan menangani tabel 'tiket_ekonomi'."""

    def __init__(self, id_tiket=None, nama=None, harga_dasar=None, stok=None, zona=None):
        super().__init__(id_tiket, nama, harga_dasar, stok)
        self.zona = zona

    def hitung_total(self) -> float:
        """
        Tiket Ekonomi tidak punya biaya tambahan,
        total = harga dasar
        """
        if self.harga_dasar is None:
            return 0.0
        return self.harga_dasar

    def select_data_full(self):
        """Mengambil data lengkap Tiket Ekonomi dari tabel 'tiket' dan 'tiket_ekonomi'."""
        sql = """
        SELECT t.id_tiket, t.nama, t.harga_dasar, t.stok, te.zona
        FROM tiket t
        JOIN tiket_ekonomi te ON t.id_tiket = te.id_tiket
        """
        mycursor.execute(sql)
        return mycursor.fetchall()

    def insert_data(self):
        """Menyimpan data baru ke tabel 'tiket' dan 'tiket_ekonomi'."""
        try:
            sql_tiket = """
            INSERT INTO tiket (nama, harga_dasar, stok)
            VALUES (%s, %s, %s)
            """
            mycursor.execute(sql_tiket, (self.nama, self.harga_dasar, self.stok))
            self.id_tiket = mycursor.lastrowid

            sql_eko = """
            INSERT INTO tiket_ekonomi (id_tiket, zona)
            VALUES (%s, %s)
            """
            mycursor.execute(sql_eko, (self.id_tiket, self.zona))

            mydb.commit()
            return True
        except Exception as e:
            mydb.rollback()
            print(f"Error saat insert data Ekonomi: {e}")
            return False

    def update_data(self):
        """Memperbarui data di tabel 'tiket' dan 'tiket_ekonomi'."""
        if self.id_tiket is None:
            return False

        try:
            sql_tiket = """
            UPDATE tiket
            SET nama = %s, harga_dasar = %s, stok = %s
            WHERE id_tiket = %s
            """
            mycursor.execute(
                sql_tiket,
                (self.nama, self.harga_dasar, self.stok, self.id_tiket)
            )

            sql_eko = """
            UPDATE tiket_ekonomi
            SET zona = %s
            WHERE id_tiket = %s
            """
            mycursor.execute(sql_eko, (self.zona, self.id_tiket))

            mydb.commit()
            return True
        except Exception as e:
            mydb.rollback()
            print(f"Error saat update data Ekonomi: {e}")
            return False

    def delete_data(self):
        """
        Menghapus data dari tabel 'tiket'
        (otomatis menghapus tiket_ekonomi karena CASCADE)
        """
        if self.id_tiket is None:
            return False

        try:
            sql = "DELETE FROM tiket WHERE id_tiket = %s"
            mycursor.execute(sql, (self.id_tiket,))
            mydb.commit()
            return True
        except Exception as e:
            mydb.rollback()
            print(f"Error saat delete data Ekonomi: {e}")
            return False
