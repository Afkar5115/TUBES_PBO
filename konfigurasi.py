# konfigurasi.py
import os

# Direktori dasar proyek
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Konfigurasi database untuk tugas
NAMA_DB = 'tugas_mahasiswa_ti1b.db'
DB_PATH = os.path.join(BASE_DIR, NAMA_DB)

# Daftar pilihan untuk UI
MATA_KULIAH = [
    "B. Inggris", 
    "Database", 
    "Embeded System", 
    "Kecerdasan Buatan", 
    "Jaringan Komputer", 
    "Kewarganegaraan",
    "PBO", 
    "Statistika"
]

TINGKATAN_TUGAS = ["Standar", "Penting", "Urgent"]

KATEGORI_DEFAULT = "PBO"