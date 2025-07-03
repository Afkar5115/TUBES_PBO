# app_tugas.py
import streamlit as st
import datetime
import pandas as pd
from manajer_tugas import ManajerTugas
from konfigurasi import MATA_KULIAH, TINGKATAN_TUGAS
from model import Tugas

# --- Konfigurasi Halaman dan Tema ---
st.set_page_config(
    page_title="Pencatat Tugas TI-1B",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS Kustom untuk Tampilan Tema Gelap yang Lebih Baik ---
# Definisikan CSS kustom untuk efek "menyala"
CUSTOM_CSS = """
<style>
/* Mengubah warna latar belakang utama menjadi lebih gelap */
[data-testid="stAppViewContainer"] {
    background-color: #121212;
    color: #EAEAEA; /* Warna teks default yang terang */
}

/* Kustomisasi sidebar dengan border menyala */
[data-testid="stSidebar"] {
    background-color: #1E1E1E;
    border-right: 1px solid #00BFFF;
}

/* --- PERBAIKAN TOMBOL SIMPAN --- */
/* Kustomisasi tombol dengan efek menyala */
.stButton>button {
    border-radius: 20px;
    border: 1px solid #00BFFF;
    background-color: #00BFFF; /* Latar belakang solid */
    color: #1E1E1E; /* Warna teks gelap agar kontras */
    font-weight: bold; /* Menebalkan teks */
    transition: all 0.3s ease-in-out;
    box-shadow: 0 0 8px rgba(0, 191, 255, 0.6);
}
.stButton>button:hover {
    border: 1px solid #FFFFFF;
    background-color: #87CEFA; /* Warna biru lebih terang saat hover */
    color: #121212;
    box-shadow: 0 0 20px #00BFFF;
    text-shadow: none;
}
.stButton>button:active {
    background-color: #009ACD; /* Warna biru lebih gelap saat ditekan */
    border-color: #009ACD;
}

/* Memberi border menyala pada container form */
.form-container {
    border: 1px solid #00BFFF;
    border-radius: 10px;
    padding: 25px;
    background-color: #1E1E1E;
    box-shadow: 0 0 12px rgba(0, 191, 255, 0.4);
}

/* Memberi warna menyala pada label input */
label {
    color: #00BFFF !important; /* Menggunakan !important untuk memastikan gaya diterapkan */
}

/* Kustomisasi dataframe */
.stDataFrame {
    border: 1px solid #4A4A4A;
    border-radius: 10px;
    background-color: #1E1E1E;
}

/* --- PERBAIKAN SIDEBAR --- */

/* Teks menu navigasi di sidebar menjadi putih */
[data-testid="stSidebar"] .st-emotion-cache-1y4p8pa {
    color: #FFFFFF; /* Warna default putih */
    transition: all 0.3s ease;
}

/* Teks menu navigasi yang sedang aktif/dipilih tetap menyala */
[data-testid="stSidebar"] .st-emotion-cache-1y4p8pa:has(input:checked) {
    color: #FFFFFF;
    text-shadow: 0 0 6px #00BFFF, 0 0 12px #00BFFF;
}


/* Kustomisasi kotak info di sidebar agar lebih menyala */
[data-testid="stInfo"] {
    background-color: rgba(0, 191, 255, 0.1);
    border: 1px solid rgba(0, 191, 255, 0.5);
    border-radius: 10px;
    color: #87CEFA; /* Warna teks biru langit terang */
    text-shadow: 0 0 4px rgba(135, 206, 250, 0.8); /* Efek glow halus */
}

/* Kustomisasi caption versi di sidebar */
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: #888888; /* Warna abu-abu terang agar lebih terlihat */
}


</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# --- Inisialisasi Manajer Tugas ---
@st.cache_resource
def get_tugas_manager():
    """Menginisialisasi ManajerTugas dan menyimpan resource dalam cache."""
    return ManajerTugas()

manajer = get_tugas_manager()

# --- Halaman UI ---

def halaman_input(manajer: ManajerTugas):
    """Halaman untuk menambah tugas baru."""
    st.title("📚 Pencatat Tugas Mahasiswa TI-1B")
    st.write("Tambahkan tugas baru agar tidak ada yang terlewat.")
    
    # Menggunakan container untuk form agar terlihat lebih rapi
    with st.container():
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        with st.form("form_tugas_baru", clear_on_submit=True):
            deskripsi = st.text_input("Deskripsi Tugas*", placeholder="Contoh: Mengerjakan Jobsheet 1 PBO")
            
            col1, col2 = st.columns(2)
            with col1:
                kategori = st.selectbox("Mata Kuliah*:", MATA_KULIAH, index=6) # Default PBO
            with col2:
                tingkatan = st.selectbox("Tingkatan Prioritas*:", TINGKATAN_TUGAS, index=0) # Default Standar
            
            tanggal = st.date_input("🗓️ Tanggal Deadline*:", value=datetime.date.today())
            
            submitted = st.form_submit_button("💾 Simpan Tugas")
            
            if submitted:
                if not deskripsi:
                    st.warning("Deskripsi tugas wajib diisi!", icon="⚠️")
                else:
                    with st.spinner("Menyimpan..."):
                        tugas_baru = Tugas(deskripsi, tingkatan, kategori, tanggal)
                        if manajer.tambah_tugas(tugas_baru):
                            st.success("Tugas berhasil disimpan!", icon="✅")
                            st.cache_data.clear()
                        else:
                            st.error("Gagal menyimpan tugas.", icon="❌")
        st.markdown('</div>', unsafe_allow_html=True)


def halaman_riwayat(manajer: ManajerTugas):
    """Halaman untuk menampilkan dan menghapus riwayat tugas."""
    st.title("🗂️ Riwayat Semua Tugas")
    
    with st.spinner("Memuat riwayat..."):
        df_tugas = manajer.get_dataframe_tugas()
    
    if df_tugas.empty:
        st.info("Belum ada tugas yang tercatat. Silakan tambahkan tugas baru pada menu 'Tambah Tugas'.")
    else:
        st.dataframe(df_tugas, use_container_width=True)

    st.markdown("---")
    
    # Bagian untuk menghapus tugas
    with st.expander("🗑️ Hapus Tugas"):
        id_tugas = st.number_input(
            "Masukkan ID Tugas yang ingin dihapus:", 
            min_value=1, 
            step=1, 
            value=None, 
            placeholder="Ketik ID dari tabel di atas..."
        )
        
        if st.button("Konfirmasi Hapus"):
            if id_tugas is not None:
                with st.spinner("Menghapus..."):
                    if manajer.hapus_tugas(int(id_tugas)):
                        st.success(f"Tugas dengan ID {id_tugas} berhasil dihapus.", icon="✅")
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error(f"Gagal menghapus tugas ID {id_tugas}. Pastikan ID valid.", icon="❌")
            else:
                st.warning("Mohon masukkan ID tugas yang valid untuk dihapus.")

# --- Logika Aplikasi Utama ---
def main():
    """Fungsi utama untuk menjalankan aplikasi Streamlit."""
    with st.sidebar:
        st.header("Menu Navigasi")
        menu_pilihan = st.radio(
            "Pilih Halaman:", 
            ["➕ Tambah Tugas", "🗂️ Riwayat Tugas"], 
            key="menu_utama",
            label_visibility="collapsed"
        )
        st.markdown("---")
        st.info("Aplikasi ini dibuat untuk membantu mahasiswa TI-1B dalam mengelola tugas kuliah.")
        st.caption("Create by Afkar")

    if menu_pilihan == "➕ Tambah Tugas":
        halaman_input(manajer)
    elif menu_pilihan == "🗂️ Riwayat Tugas":
        halaman_riwayat(manajer)

if __name__ == "__main__":
    main()
