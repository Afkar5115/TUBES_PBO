# model.py
import datetime

class Tugas:
    """
    Merepresentasikan satu entitas tugas mahasiswa (Data Class).
    """
    def __init__(self, deskripsi: str, tingkatan: str, kategori: str,
                 tanggal: datetime.date | str, id_tugas: int | None = None):
        """
        Inisialisasi objek Tugas.
        """
        self.id = id_tugas
        self.deskripsi = str(deskripsi) if deskripsi else "Tanpa Deskripsi"
        self.tingkatan = str(tingkatan) if tingkatan else "Standar"
        self.kategori = str(kategori) # Kategori (Mata Kuliah)
        
        # Validasi dan konversi tanggal
        if isinstance(tanggal, datetime.date):
            self.tanggal = tanggal
        elif isinstance(tanggal, str):
            try:
                self.tanggal = datetime.datetime.strptime(tanggal, "%Y-%m-%d").date()
            except ValueError:
                self.tanggal = datetime.date.today()
        else:
            self.tanggal = datetime.date.today()

    def __repr__(self) -> str:
        """
        Representasi string dari objek Tugas untuk debugging.
        """
        tgl_str = self.tanggal.strftime('%d-%m-%Y')
        return (f"Tugas(ID: {self.id}, Tgl: {tgl_str}, Tingkat: '{self.tingkatan}', "
                f"Matkul: '{self.kategori}', Desc: '{self.deskripsi}')")

    def to_dict(self) -> dict:
        """
        Mengubah objek Tugas menjadi dictionary.
        """
        return {
            "deskripsi": self.deskripsi,
            "tingkatan": self.tingkatan,
            "kategori": self.kategori,
            "tanggal": self.tanggal.strftime("%Y-%m-%d")
        }