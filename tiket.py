# tiket.py

from connection import mycursor, mydb

class Tiket:
    """
    Kelas dasar Tiket. Menyediakan properti umum (nama, harga_dasar, stok)
    dan metode database yang berkaitan dengan tabel 'tiket'.
    """
    def __init__(self, id_tiket=None, nama=None, harga_dasar=None, stok=None):
        self.id_tiket = id_tiket
        self.nama = nama
        self.harga_dasar = harga_dasar
        self.stok = stok

    # --- Metode Database (Read/Update Umum) ---
    
    def select_data(self):
        """Mengambil semua data dari tabel 'tiket'."""
        sql = "SELECT id_tiket, nama, harga_dasar, stok FROM tiket"
        mycursor.execute(sql)
        return mycursor.fetchall()

    def select_data_by_id(self, id_tiket):
        """Mengambil data tiket berdasarkan ID."""
        sql = """
        SELECT id_tiket, nama, harga_dasar, stok
        FROM tiket
        WHERE id_tiket = %s
        """
        mycursor.execute(sql, (id_tiket,))
        return mycursor.fetchone()

    def update_stok(self, id_tiket, jumlah):
        """Mengurangi stok tiket setelah pembelian."""
        sql = """
        UPDATE tiket
        SET stok = stok - %s
        WHERE id_tiket = %s
        """
        mycursor.execute(sql, (jumlah, id_tiket))
        mydb.commit()

    # --- Metode Abstrak Sesuai UML ---
    
    def get_harga(self) -> float:
        """Mengembalikan harga dasar."""
        return self.harga_dasar

    def tampilkan_info(self) -> str:
        """Menampilkan informasi umum tiket."""
        return f"Nama: {self.nama}, Harga Dasar: {self.harga_dasar}, Stok: {self.stok}"
    
    def hitung_total(self) -> float:
        """Metode ini harus diimplementasikan oleh subkelas (TiketVIP/Ekonomi)."""
        # Sesuai UML, ini adalah metode abstrak
        raise NotImplementedError("Subkelas harus mengimplementasikan hitung_total()")