import streamlit as st
import base64
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from io import BytesIO

st.set_page_config(page_title="JPN Selangor", layout="wide")
st.set_page_config(page_title="JPN Selangor", layout="wide")

# Sembunyikan header + footer + manage app Streamlit
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div[data-testid="stDecoration"] {display:none;}
    div[data-testid="stStatusWidget"] {display:none;}
    
    /* Sorok semua button atas kanan */
    div[data-testid="stToolbar"] {
        display: none !important;
    }
    
    /* Paksa button buka sidebar keluar */
    button[kind="header"] {
        display: block !important;
        position: fixed !important;
        top: 1rem !important;
        left: 1rem !important;
        z-index: 9999 !important;
    }
    </style>
    """
st.markdown(hide_st_style, unsafe_allow_html=True)
# Kredit kecil di atas
st.markdown("""
    <div style='text-align: right; font-size: 10px; color: grey; margin-bottom: -10px;'>
        Created by: Akashah Ismail
    </div>
    """, unsafe_allow_html=True)
# ========== DATA ASAL ==========
DATA_ASAL = {
    "Petaling Perdana": {"A-Sekolah Kerajaan": 13671, "B-Sekolah Agensi": 0, "C-Sekolah Bantuan Kerajaan": 800, "D-Sekolah Swasta": 1200, "E-Calon Persendirian": 300, "Penyelia Kawasan": 15, "Ketua Pengawas": 25, "Timbalan Ketua Pengawas": 25, "Pengawas": 100, "Pengemas Bilik": 15, "Sukarelawan": 50},
    "Petaling Utama": {"A-Sekolah Kerajaan": 5500, "B-Sekolah Agensi": 160, "C-Sekolah Bantuan Kerajaan": 850, "D-Sekolah Swasta": 1300, "E-Calon Persendirian": 320, "Penyelia Kawasan": 16, "Ketua Pengawas": 27, "Timbalan Ketua Pengawas": 27, "Pengawas": 110, "Pengemas Bilik": 16, "Sukarelawan": 55},
    "Hulu Langat": {"A-Sekolah Kerajaan": 4800, "B-Sekolah Agensi": 120, "C-Sekolah Bantuan Kerajaan": 650, "D-Sekolah Swasta": 900, "E-Calon Persendirian": 250, "Penyelia Kawasan": 12, "Ketua Pengawas": 22, "Timbalan Ketua Pengawas": 22, "Pengawas": 90, "Pengemas Bilik": 14, "Sukarelawan": 45},
    "Gombak": {"A-Sekolah Kerajaan": 4500, "B-Sekolah Agensi": 100, "C-Sekolah Bantuan Kerajaan": 700, "D-Sekolah Swasta": 1100, "E-Calon Persendirian": 200, "Penyelia Kawasan": 14, "Ketua Pengawas": 20, "Timbalan Ketua Pengawas": 20, "Pengawas": 85, "Pengemas Bilik": 12, "Sukarelawan": 40},
    "Klang": {"A-Sekolah Kerajaan": 5000, "B-Sekolah Agensi": 130, "C-Sekolah Bantuan Kerajaan": 750, "D-Sekolah Swasta": 850, "E-Calon Persendirian": 280, "Penyelia Kawasan": 13, "Ketua Pengawas": 23, "Timbalan Ketua Pengawas": 23, "Pengawas": 95, "Pengemas Bilik": 13, "Sukarelawan": 48},
    "Kuala Langat": {"A-Sekolah Kerajaan": 2100, "B-Sekolah Agensi": 50, "C-Sekolah Bantuan Kerajaan": 300, "D-Sekolah Swasta": 200, "E-Calon Persendirian": 100, "Penyelia Kawasan": 8, "Ketua Pengawas": 10, "Timbalan Ketua Pengawas": 10, "Pengawas": 40, "Pengemas Bilik": 7, "Sukarelawan": 20},
    "Kuala Selangor": {"A-Sekolah Kerajaan": 2300, "B-Sekolah Agensi": 60, "C-Sekolah Bantuan Kerajaan": 350, "D-Sekolah Swasta": 250, "E-Calon Persendirian": 120, "Penyelia Kawasan": 9, "Ketua Pengawas": 11, "Timbalan Ketua Pengawas": 11, "Pengawas": 45, "Pengemas Bilik": 8, "Sukarelawan": 25},
    "Hulu Selangor": {"A-Sekolah Kerajaan": 2000, "B-Sekolah Agensi": 40, "C-Sekolah Bantuan Kerajaan": 280, "D-Sekolah Swasta": 180, "E-Calon Persendirian": 90, "Penyelia Kawasan": 7, "Ketua Pengawas": 9, "Timbalan Ketua Pengawas": 9, "Pengawas": 35, "Pengemas Bilik": 6, "Sukarelawan": 18},
    "Sabak Bernam": {"A-Sekolah Kerajaan": 1500, "B-Sekolah Agensi": 30, "C-Sekolah Bantuan Kerajaan": 200, "D-Sekolah Swasta": 100, "E-Calon Persendirian": 70, "Penyelia Kawasan": 6, "Ketua Pengawas": 7, "Timbalan Ketua Pengawas": 7, "Pengawas": 28, "Pengemas Bilik": 5, "Sukarelawan": 15},
    "Sepang": {"A-Sekolah Kerajaan": 2600, "B-Sekolah Agensi": 70, "C-Sekolah Bantuan Kerajaan": 400, "D-Sekolah Swasta": 600, "E-Calon Persendirian": 150, "Penyelia Kawasan": 10, "Ketua Pengawas": 12, "Timbalan Ketua Pengawas": 12, "Pengawas": 50, "Pengemas Bilik": 9, "Sukarelawan": 30},
}

JENIS_CALON = ["Semua Jenis"] + ["A-Sekolah Kerajaan", "B-Sekolah Agensi", "C-Sekolah Bantuan Kerajaan", "D-Sekolah Swasta", "E-Calon Persendirian"]
JENIS_PETUGAS = ["Semua Jawatan"] + ["Penyelia Kawasan", "Ketua Pengawas", "Timbalan Ketua Pengawas", "Pengawas", "Pengemas Bilik", "Sukarelawan"]
SEMUA_KATEGORI = JENIS_CALON[1:] + JENIS_PETUGAS[1:]

KOD_PPD = {"Petaling Perdana": "BH", "Petaling Utama": "BK", "Hulu Langat": "BD", "Gombak": "BG", "Klang": "BA", "Kuala Langat": "BB", "Kuala Selangor": "BC", "Hulu Selangor": "BE", "Sabak Bernam": "BF", "Sepang": "BJ"}

USERS = {
    "admin": {"password": "jpn2025", "role": "Admin", "tahap": "JPN"},
    "ppd_petaling_perdana": {"password": "ppdpp2025", "role": "PPD", "daerah": "Petaling Perdana"},
    "ppd_petaling_utama": {"password": "ppdpu2025", "role": "PPD", "daerah": "Petaling Utama"},
    "ppd_hulu_langat": {"password": "ppdhl2025", "role": "PPD", "daerah": "Hulu Langat"},
    "ppd_gombak": {"password": "ppdgk2025", "role": "PPD", "daerah": "Gombak"},
    "ppd_klang": {"password": "ppdkl2025", "role": "PPD", "daerah": "Klang"},
    "ppd_kuala_langat": {"password": "ppdklg2025", "role": "PPD", "daerah": "Kuala Langat"},
    "ppd_kuala_selangor": {"password": "ppdks2025", "role": "PPD", "daerah": "Kuala Selangor"},
    "ppd_hulu_selangor": {"password": "ppdhs2025", "role": "PPD", "daerah": "Hulu Selangor"},
    "ppd_sabak_bernam": {"password": "ppdsb2025", "role": "PPD", "daerah": "Sabak Bernam"},
    "ppd_sepang": {"password": "ppdsp2025", "role": "PPD", "daerah": "Sepang"},
}

FILE_EXCEL = "data_v1.1.xlsx"
SHEET_PUSAT = "selenggara_pusat"
SHEET_MP = "MataPelajaran"
COLUMNS_PUSAT = ["Kod_PPD","No_Pusat","Nama_Pusat","Bil_Calon_Pusat","Nama_Bilik_Kebal","Dikemaskini_Oleh","Tarikh_Kemaskini"]
COLUMNS_MP = ["Kod_PPD","No_Pusat","Nama_Pusat","KodMP","NamaMP","Kertas","Tarikh"]

LINK_PENGURUSAN = "https://drive.google.com/drive/folders/193ELWVyPDORTVE7ZSVe2B3rsZILkg7f6?usp=drive_link"

# ========== FUNGSI EXCEL ==========
def load_data_pusat():
    if os.path.exists(FILE_EXCEL):
        try: return pd.read_excel(FILE_EXCEL, sheet_name=SHEET_PUSAT, engine='openpyxl', dtype=str)
        except: return pd.DataFrame(columns=COLUMNS_PUSAT)
    else: return pd.DataFrame(columns=COLUMNS_PUSAT)

def load_data_mp():
    if os.path.exists(FILE_EXCEL):
        try: return pd.read_excel(FILE_EXCEL, sheet_name=SHEET_MP, engine='openpyxl', dtype=str)
        except: return pd.DataFrame(columns=COLUMNS_MP)
    else: return pd.DataFrame(columns=COLUMNS_MP)

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer: df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

def simpan_ke_excel():
    with pd.ExcelWriter(FILE_EXCEL, engine='openpyxl', mode='w') as writer:
        st.session_state["data_pusat"].to_excel(writer, sheet_name=SHEET_PUSAT, index=False)
        st.session_state["data_mp"].to_excel(writer, sheet_name=SHEET_MP, index=False)

def simpan_data_pusat(kod_ppd, no_pusat, nama_pusat, bil_calon, nama_kebal, dikemaskini_oleh):
    df = st.session_state["data_pusat"]
    df = df[df['No_Pusat']!= no_pusat]
    data_baru = pd.DataFrame([{'Kod_PPD': kod_ppd, 'No_Pusat': no_pusat, 'Nama_Pusat': nama_pusat, 'Bil_Calon_Pusat': bil_calon, 'Nama_Bilik_Kebal': nama_kebal, 'Dikemaskini_Oleh': dikemaskini_oleh, 'Tarikh_Kemaskini': datetime.now().strftime("%Y-%m-%d %H:%M")}])
    st.session_state["data_pusat"] = pd.concat([df, data_baru], ignore_index=True)
    simpan_ke_excel()

def simpan_data_mp(df_baru):
    st.session_state["data_mp"] = df_baru
    simpan_ke_excel()

def upload_pukal(uploaded_file, dikemaskini_oleh):
    try:
        df_upload = pd.read_excel(uploaded_file, engine='openpyxl', dtype=str)
        df_upload.columns = df_upload.columns.str.strip()
        df_upload = df_upload[COLUMNS_PUSAT]
        df_upload['Dikemaskini_Oleh'] = dikemaskini_oleh
        df_upload['Tarikh_Kemaskini'] = datetime.now().strftime("%Y-%m-%d %H:%M")
        df_lama = st.session_state["data_pusat"]
        df_gabung = pd.concat([df_lama, df_upload]).drop_duplicates(subset=['No_Pusat'], keep='last')
        st.session_state["data_pusat"] = df_gabung
        simpan_ke_excel()
        return True, f"Berjaya upload {len(df_upload)} rekod"
    except Exception as e: return False, f"Ralat: {e}. Pastikan header sama: {COLUMNS_PUSAT}"

# ========== SESSION STATE ==========
if "data_calon" not in st.session_state: st.session_state["data_calon"] = DATA_ASAL
if "data_pusat" not in st.session_state: st.session_state["data_pusat"] = load_data_pusat()
if "data_mp" not in st.session_state: st.session_state["data_mp"] = load_data_mp()
if "editor_login" not in st.session_state: st.session_state["editor_login"] = False
if "show_editor" not in st.session_state: st.session_state["show_editor"] = False
if "pdf_jadual" not in st.session_state: st.session_state["pdf_jadual"] = None
if "menu" not in st.session_state: st.session_state["menu"] = "Dashboard"

# ========== FUNGSI LAIN ==========
def login_editor():
    with st.form("login_form"):
        st.markdown("#### 🔒 Log Masuk")
        username = st.text_input("Nama Pengguna", key="user_login")
        password = st.text_input("Kata Laluan", type="password", key="pass_login")
        submitted = st.form_submit_button("Log Masuk", use_container_width=True, type="primary")
        if submitted:
            if username in USERS and USERS[username]["password"] == password:
                st.session_state["editor_login"] = True; st.session_state["username"] = username; st.session_state["role"] = USERS[username]["role"]
                if USERS[username]["role"] == "PPD": st.session_state["daerah_ppd"] = USERS[username]["daerah"]; st.session_state["kod_ppd"] = KOD_PPD[USERS[username]["daerah"]]
                st.success("Berjaya!"); st.rerun()
            else: st.error("Nama pengguna atau kata laluan salah!")

def page_selenggara_pusat():
    st.header("⚙️ Selenggara Data")
    if not st.session_state.get("editor_login", False): st.warning("Sila login dahulu di menu Selenggara Data"); return

    tab1, tab2 = st.tabs(["🏫 Selenggara Pusat", "📚 Selenggara Mata Pelajaran"])

    with tab1:
        role = st.session_state["role"]
        if role == "Admin":
            pilihan_ppd = st.selectbox("Pilih PPD untuk kemaskini", list(KOD_PPD.values()))
            st.write("---")
            with st.expander("📤 Upload Data Pukal 1000 Pusat - Admin Sahaja"):
                st.download_button("⬇️ Download Template Excel", to_excel(pd.DataFrame(columns=COLUMNS_PUSAT)), "template_pusat.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                uploaded_file = st.file_uploader("Upload File Excel", type=['xlsx'], key="up_pusat")
                if uploaded_file:
                    ok, msg = upload_pukal(uploaded_file, st.session_state["username"])
                    if ok: st.success(msg); st.rerun()
                    else: st.error(msg)
        else: pilihan_ppd = st.session_state["kod_ppd"]; st.info(f"Anda login sebagai PPD: {st.session_state['daerah_ppd']} - {pilihan_ppd}")

        with st.form("form_pusat"):
            col1, col2 = st.columns(2)
            with col1: no_pusat = st.text_input("No Pusat *"); nama_pusat = st.text_input("Nama Pusat *")
            with col2: bil_calon = st.number_input("Bilangan Calon Ikut Pusat", min_value=0, step=1); nama_kebal = st.text_input("Nama Bilik Kebal")
            submitted = st.form_submit_button("💾 Simpan Data", type="primary", use_container_width=True)
            if submitted:
                if no_pusat == "" or nama_pusat == "": st.error("No Pusat dan Nama Pusat wajib diisi")
                else: simpan_data_pusat(pilihan_ppd, no_pusat, nama_pusat, bil_calon, nama_kebal, st.session_state["username"]); st.success("Data berjaya disimpan!"); st.rerun()
        st.write("---"); st.subheader(f"Senarai Pusat di {pilihan_ppd}")
        df_tunjuk = st.session_state["data_pusat"][st.session_state["data_pusat"]['Kod_PPD'] == pilihan_ppd]
        st.dataframe(df_tunjuk, use_container_width=True)

    with tab2:
        st.subheader("1. Muat Turun Template Mata Pelajaran")
        st.download_button("📥 Muat Turun Template MataPelajaran.xlsx", to_excel(pd.DataFrame(columns=COLUMNS_MP)), "template_matapelajaran.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
        st.caption("Isi No_Pusat mesti sama dengan dalam data Pusat")
        st.subheader("2. Muat Naik Fail Mata Pelajaran")
        uploaded_file_mp = st.file_uploader("Pilih fail mata pelajaran", type=["xlsx"], key="up_mp")
        if uploaded_file_mp:
            try:
                df_baru_mp = pd.read_excel(uploaded_file_mp, dtype=str)
                df_baru_mp.columns = df_baru_mp.columns.str.strip()
                st.success("Fail berjaya dibaca!"); st.dataframe(df_baru_mp.head(), use_container_width=True)
                if st.button("✅ Sahkan & Simpan Data Mata Pelajaran", use_container_width=True, key="save_mp"):
                    simpan_data_mp(df_baru_mp); st.success("Data Mata Pelajaran berjaya dikemaskini!"); st.rerun()
            except Exception as e: st.error(f"Ralat: {e}")

def page_cari_mp():
    st.header("📚 Carian Mata Pelajaran Mengikut Pusat")
    df_mp = st.session_state["data_mp"]
    if df_mp.empty: st.warning("Sheet 'MataPelajaran' masih kosong. Sila isi di menu Selenggara Data > Selenggara Mata Pelajaran")
    else:
        col1, col2, col3 = st.columns([2,2,1])
        with col1: cari_kod = st.text_input("1. Masukkan Kod Mata Pelajaran", placeholder="Contoh: 1449")
        with col2: cari_nama = st.text_input("2. ATAU Nama Mata Pelajaran", placeholder="Contoh: MATEMATIK")
        with col3: cari_kertas = st.selectbox("3. Pilih Kertas", ["Semua", "1", "2", "3"])
        if st.button("🔍 Cari Sekarang", type="primary", use_container_width=True):
            df_filter = df_mp.copy()
            if st.session_state.get("role") == "PPD": df_filter = df_filter[df_filter["Kod_PPD"] == st.session_state["kod_ppd"]]
            if cari_kod: df_filter = df_filter[df_filter["KodMP"].str.contains(cari_kod, case=False, na=False)]
            elif cari_nama: df_filter = df_filter[df_filter["NamaMP"].str.contains(cari_nama, case=False, na=False)]
            if cari_kertas!= "Semua": df_filter = df_filter[df_filter["Kertas"].astype(str) == cari_kertas]
            if not df_filter.empty:
                st.success(f"✅ Jumpa {len(df_filter)} rekod")
                df_output = df_filter[COLUMNS_MP].drop_duplicates()
                st.dataframe(df_output, use_container_width=True)
                csv = df_output.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Export Hasil Carian ke Excel", csv, f"hasil_carian_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv", use_container_width=True)
            else: st.error("⚠️ Tiada pusat yang menawarkan mata pelajaran tersebut")

def page_senarai_pusat():
    st.header("📋 Senarai Pusat Peperiksaan")
    df_pusat = st.session_state["data_pusat"]
    if df_pusat.empty:
        st.warning("Tiada data pusat. Sila masukkan data di menu Selenggara Data > Selenggara Pusat")
    else:
        if st.session_state.get("role") == "PPD":
            df_pusat = df_pusat[df_pusat["Kod_PPD"] == st.session_state["kod_ppd"]]
            st.info(f"Menunjukkan senarai pusat untuk: {st.session_state['daerah_ppd']}")

        df_output = df_pusat[["Kod_PPD", "No_Pusat", "Nama_Pusat", "Nama_Bilik_Kebal", "Bil_Calon_Pusat"]].copy()
        df_output = df_output.sort_values(by=["Kod_PPD", "No_Pusat"])

        st.metric("Jumlah Pusat", len(df_output))
        st.dataframe(df_output, use_container_width=True, hide_index=True)

        csv = df_output.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export Senarai Pusat ke Excel", csv, f"senarai_pusat_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv", use_container_width=True)

# ========== HEADER ==========
st.markdown("""<style>.block-container { padding-top: 2.5rem!important; }</style>""", unsafe_allow_html=True)
col1, col2 = st.columns([1, 5])
with col1:
    if os.path.exists("logo.png"):
        with open("logo.png", "rb") as f: logo_bytes = f.read()
        logo_b64 = base64.b64encode(logo_bytes).decode()
        st.markdown(f'<img src="data:image/png;base64,{logo_b64}" width="100">', unsafe_allow_html=True)
with col2:
    st.markdown("<h3 style='color:#0A2A66; margin-bottom:0px;'>JABATAN PENDIDIKAN SELANGOR</h3>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#0A2A66; margin-top:-8px;'>SEKTOR PENTAKSIRAN DAN PEPERIKSAAN</h4>", unsafe_allow_html=True)
st.markdown("<h4 style='color:#0A2A66; border-bottom:2px solid #0A2A66; padding-bottom:5px;'>SIJIL PELAJARAN MALAYSIA</h4>", unsafe_allow_html=True)
st.write("---")

# ========== SIDEBAR ==========
with st.sidebar:
    st.markdown("### Menu")
    if st.button("📊 Dashboard", use_container_width=True): st.session_state["menu"] = "Dashboard"; st.rerun()
    if st.button("📅 Jadual Waktu", use_container_width=True): st.session_state["menu"] = "Jadual"; st.rerun()
    if st.button("📋 Senarai Pusat", use_container_width=True): st.session_state["menu"] = "SenaraiPusat"; st.rerun()
    if st.button("📚 Cari Mata Pelajaran", use_container_width=True): st.session_state["menu"] = "CariMP"; st.rerun()
    if st.button("🛠️ Selenggara Data", use_container_width=True): st.session_state["show_editor"] = not st.session_state["show_editor"]; st.session_state["menu"] = "Dashboard"

    st.write("---")
    st.markdown("### 🔗 Pautan Sistem Lain")
    st.link_button("1. SPPAT", "https://sppat.moe.gov.my", use_container_width=True)
    st.link_button("2. ELP Portal", "https://elp.moe.gov.my/eportal/login", use_container_width=True)
    if st.session_state.get("editor_login", False): st.link_button("3. Selenggara Calon PPD", "https://script.google.com/macros/s/AKfycbwav3jbWQEkTW2yTK9PnanlItxPM5NpCHADLNb_BRjY4hmsale257tSqMsRTdqv88HA/exec", use_container_width=True)

    if st.session_state.get("editor_login", False):
        st.write("---")
        st.markdown("### 📁 Pautan Pengurusan")
        st.link_button("4. Pengurusan", LINK_PENGURUSAN, use_container_width=True, type="primary")

    st.write("---")
    if st.session_state.get("editor_login", False):
        if st.button("🛠️ Selenggara Pusat", use_container_width=True): st.session_state["menu"] = "Selenggara"; st.rerun()

    if st.session_state["show_editor"]:
        st.write("---")
        if not st.session_state.get("editor_login", False): login_editor()
        else:
            st.success(f"Login: **{st.session_state['username']}**")
            st.caption(f"Role: **{st.session_state['role']}**")
            if st.button("Log Keluar", use_container_width=True): st.session_state["editor_login"] = False; st.session_state["show_editor"] = False; st.session_state["menu"] = "Dashboard"; st.rerun()

    if st.session_state["menu"] == "Dashboard":
        st.write("---")
        data = st.session_state["data_calon"]
        daerah_list = ["Semua Daerah"] + list(data.keys())
        daerah = st.selectbox("Pilih Daerah:", daerah_list, key="filter_daerah_v2")
        jenis_data = st.selectbox("Pilih Data:", ["Calon", "Petugas", "Semua"], key="filter_jenis_v2")
        if jenis_data == "Calon": sub_filter = st.selectbox("Pilih Jenis Calon:", JENIS_CALON, key="filter_sub1_v2")
        elif jenis_data == "Petugas": sub_filter = st.selectbox("Pilih Jawatan Petugas:", JENIS_PETUGAS, key="filter_sub2_v2")
        else: sub_filter = "Semua"
    else: daerah, jenis_data, sub_filter = "Semua Daerah", "Semua", "Semua"

# ========== PAPARAN UTAMA ==========
if st.session_state["menu"] == "Dashboard":
    data = st.session_state["data_calon"]
    if jenis_data == "Calon": kategori_list = JENIS_CALON[1:] if sub_filter == "Semua Jenis" else [sub_filter]
    elif jenis_data == "Petugas": kategori_list = JENIS_PETUGAS[1:] if sub_filter == "Semua Jawatan" else [sub_filter]
    else: kategori_list = SEMUA_KATEGORI
    jumlah = sum(sum(data[d][k] for k in kategori_list) for d in data) if daerah == "Semua Daerah" else sum(data[daerah][k] for k in kategori_list)
    jumlah_petugas_total = sum(sum(data[d][k] for k in JENIS_PETUGAS[1:]) for d in data)
    jumlah_pusat_total = len(st.session_state["data_pusat"]) # <-- DAH FIX: KIRA SEMUA BARIS
    st.info(f"Daerah: **{daerah}** | Data: **{jenis_data}** | Filter: **{sub_filter}**")
    colA, colB, colC = st.columns(3)
    with colA: st.metric(f"Jumlah", f"{jumlah:,}")
    with colB: st.metric("Jumlah Petugas Negeri", f"{jumlah_petugas_total:,}")
    with colC: st.metric("Jumlah Rekod Pusat", f"{jumlah_pusat_total:,}") # <-- DAH FIX: TUKAR LABEL

    st.write("---")
    if jenis_data == "Calon" or jenis_data == "Semua":
        st.subheader("📊 Bilangan Calon Mengikut Daerah")
        df_calon = pd.DataFrame([{k: v[k] for k in JENIS_CALON[1:]} for v in data.values()], index=data.keys())
        if daerah!= "Semua Daerah": df_calon = df_calon.loc[[daerah]]
        if sub_filter!= "Semua Jenis" and jenis_data == "Calon": df_calon = df_calon[[sub_filter]]
        st.dataframe(df_calon, use_container_width=True)
        fig1, ax1 = plt.subplots(figsize=(10, 5)); df_calon.plot(kind='bar', ax=ax1); ax1.set_ylabel("Bilangan Calon"); ax1.set_xlabel("Daerah"); ax1.legend(title="Jenis Calon", bbox_to_anchor=(1.05, 1), loc='upper left'); plt.xticks(rotation=90); plt.tight_layout(); st.pyplot(fig1)
    if jenis_data == "Petugas" or jenis_data == "Semua":
        st.write("---"); st.subheader("👮 Bilangan Petugas Mengikut Daerah")
        df_petugas = pd.DataFrame([{k: v[k] for k in JENIS_PETUGAS[1:]} for v in data.values()], index=data.keys())
        if daerah!= "Semua Daerah": df_petugas = df_petugas.loc[[daerah]]
        if sub_filter!= "Semua Jawatan" and jenis_data == "Petugas": df_petugas = df_petugas[[sub_filter]]
        st.dataframe(df_petugas, use_container_width=True)
        fig2, ax2 = plt.subplots(figsize=(10, 5)); df_petugas.plot(kind='bar', ax=ax2); ax2.set_ylabel("Bilangan Petugas"); ax2.set_xlabel("Daerah"); ax2.legend(title="Jawatan Petugas", bbox_to_anchor=(1.05, 1), loc='upper left'); plt.xticks(rotation=90); plt.tight_layout(); st.pyplot(fig2)

elif st.session_state["menu"] == "Jadual":
    st.subheader("📅 Jadual Waktu SPM")
    st.info("Untuk kemaskini Jadual: Upload file `Jadual_Waktu_SPM.pdf` ke Github dan update LINK_JADUAL_PDF dalam kod")
    
    LINK_JADUAL_PDF = "https://raw.githubusercontent.com/akashahismail-create/sistem-jpn-selangor/main/Jadual_Waktu_SPM.pdf"
    
    st.markdown(f"[📥 Klik sini untuk Muat Turun Jadual Waktu]({LINK_JADUAL_PDF})")
    st.markdown(f'<iframe src="{LINK_JADUAL_PDF}" width="100%" height="800" type="application/pdf"></iframe>', unsafe_allow_html=True)
elif st.session_state["menu"] == "Selenggara": page_selenggara_pusat()
elif st.session_state["menu"] == "CariMP": page_cari_mp()
elif st.session_state["menu"] == "SenaraiPusat": page_senarai_pusat()

if st.session_state.get("show_editor", False) and st.session_state.get("editor_login", False):
    st.write("---"); role = st.session_state["role"]; st.subheader("🛠️ Selenggara Data Calon & Petugas")
    if role == "Admin":
        st.info("🔒 Kawasan Admin")
        with open(__file__, "r", encoding="utf-8") as f: kod_semasa = f.read()
        st.download_button(label="⬇️ Download Backup Kod Sumber V1.9", data=kod_semasa, file_name="JPN_Selangor_V1.9.py", mime="text/plain", use_container_width=True, type="primary")
        st.write("---")
    data_asal = st.session_state["data_calon"]
    if role == "PPD": daerah_list_edit = [st.session_state["daerah_ppd"]]; st.warning(f"Anda hanya boleh edit data untuk: **{daerah_list_edit[0]}**")
    else: daerah_list_edit = list(data_asal.keys())
    with st.form("form_edit_data"):
        data_baru = {}
        for d in daerah_list_edit:
            st.markdown(f"### 📍 {d}")
            st.markdown("#### **Data Calon**")
            cols_calon = st.columns(5); data_baru[d] = {}
            for i, kat in enumerate(JENIS_CALON[1:]):
                with cols_calon[i]:
                    with st.container(border=True): st.markdown(f"<div style='text-align:center; font-size:13px;'>{kat}</div>", unsafe_allow_html=True)
                    data_baru[d][kat] = st.number_input(label="", value=int(data_asal[d][kat]), key=f"{d}_{kat}", step=1, label_visibility="collapsed")
            st.markdown("#### **Data Petugas**")
            cols_petugas = st.columns(6)
            for i, kat in enumerate(JENIS_PETUGAS[1:]):
                with cols_petugas[i]:
                    with st.container(border=True): st.markdown(f"<div style='text-align:center; font-size:13px;'>{kat}</div>", unsafe_allow_html=True)
                    data_baru[d][kat] = st.number_input(label="", value=int(data_asal[d][kat]), key=f"{d}_{kat}_petugas", step=1, label_visibility="collapsed")
            st.write("---")
        submitted = st.form_submit_button("💾 Simpan Semua Perubahan", type="primary", use_container_width=True)
        if submitted: st.session_state["data_calon"].update(data_baru); st.success("Data berjaya disimpan!"); st.rerun()
