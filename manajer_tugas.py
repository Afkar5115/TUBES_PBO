# manajer_tugas.py
import sqlite3
import pandas as pd
from model import Tugas
from typing import List, Dict, Optional
import datetime
from konfigurasi import DB_PATH

class ManajerTugas:
    """Menangani semua logika bisnis dan interaksi database untuk aplikasi tugas."""

    def __init__(self, db_path=DB_PATH):
        """Inisialisasi manajer dan memastikan tabel database ada."""
        self.db_path = db_path
        self._buat_tabel_jika_tidak_ada()

    def _get_db_connection(self):
        """Membuka koneksi baru ke database."""
        try:
            return sqlite3.connect(self.db_path)
        except sqlite3.Error as e:
            print(f"Error koneksi database: {e}")
            return None

    def _buat_tabel_jika_tidak_ada(self):
        """Membuat tabel 'tugas' jika belum ada."""
        sql_create_table = """
        CREATE TABLE IF NOT EXISTS tugas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            deskripsi TEXT NOT NULL,
            tingkatan TEXT NOT NULL,
            kategori TEXT NOT NULL,
            tanggal DATE NOT NULL
        );
        """
        conn = self._get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(sql_create_table)
                conn.commit()
            except sqlite3.Error as e:
                print(f"Error saat membuat tabel: {e}")
            finally:
                conn.close()

    def tambah_tugas(self, tugas: Tugas) -> bool:
        """Menambahkan tugas baru ke database."""
        sql = "INSERT INTO tugas (deskripsi, tingkatan, kategori, tanggal) VALUES (?, ?, ?, ?);"
        params = (tugas.deskripsi, tugas.tingkatan, tugas.kategori, tugas.tanggal.strftime('%Y-%m-%d'))
        
        conn = self._get_db_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            return cursor.lastrowid is not None
        except sqlite3.Error as e:
            print(f"Error saat menambah tugas: {e}")
            conn.rollback()
            return False
        finally:
            if conn:
                conn.close()

    def get_dataframe_tugas(self) -> Optional[pd.DataFrame]:
        """Mengambil semua tugas dan mengembalikannya sebagai DataFrame."""
        sql = "SELECT id, tanggal, deskripsi, kategori, tingkatan FROM tugas ORDER BY tanggal DESC, id DESC;"
        conn = self._get_db_connection()
        if not conn:
            return pd.DataFrame() # Return empty dataframe on connection failure
            
        try:
            df = pd.read_sql_query(sql, conn)
            # Formatting untuk tampilan
            df.columns = ['ID', 'Tanggal', 'Deskripsi', 'Mata Kuliah', 'Tingkatan']
            df['Tanggal'] = pd.to_datetime(df['Tanggal']).dt.strftime('%d-%m-%Y')
            return df.set_index('ID')
        except Exception as e:
            print(f"Error saat mengambil dataframe: {e}")
            return pd.DataFrame()
        finally:
            if conn:
                conn.close()

    def hapus_tugas(self, id_tugas: int) -> bool:
        """Menghapus tugas berdasarkan ID-nya."""
        sql = "DELETE FROM tugas WHERE id = ?;"
        conn = self._get_db_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (id_tugas,))
            conn.commit()
            return cursor.rowcount > 0 # Berhasil jika ada baris yang terhapus
        except sqlite3.Error as e:
            print(f"Error saat menghapus tugas: {e}")
            conn.rollback()
            return False
        finally:
            if conn:
                conn.close()