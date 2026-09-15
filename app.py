import streamlit as st
import base64
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from io import BytesIO

st.set_page_config(page_title="JPN Selangor", layout="wide")

# ========== SOROK MENU STREAMLIT ==========
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div[data-testid="stToolbar"] {display: none;}
    [data-testid="column"]:nth-child(1) {
        background-color: #F0F2F6;
        padding: 1rem;
        border-right: 1px solid #D0D0D0;
        min-height: 100vh;
        overflow-y: auto;
    }
    </style>
    """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.markdown("<div style='text-align: right; font-size: 10px; color: grey;'>Created by: Akashah Ismail</div>", unsafe_allow_html=True)

if 'menu_state' not in st.session_state:
    st.session_state.menu_state = True

# ========== DATA ASAL - JADI BACKUP SAJA ==========
DATA_ASAL = {
    "Petaling Perdana": {"A-Sekolah Kerajaan": 13106, "B-Sekolah Agensi": 0, "C-Sekolah Bantuan Kerajaan": 0, "D-Sekolah Swasta": 571, "E-Calon Persendirian": 974, "Penyelia Kawasan": 30, "Ketua Pengawas": 91, "Timbalan Ketua Pengawas": 91, "Pengawas": 1027, "Pengemas Bilik": 91, "Sukarelawan": 50},
    "Petaling Utama": {"A-Sekolah Kerajaan": 5209, "B-Sekolah Agensi": 0, "C-Sekolah Bantuan Kerajaan": 0, "D-Sekolah Swasta": 317, "E-Calon Persendirian": 491, "Penyelia Kawasan": 22, "Ketua Pengawas": 43, "Timbalan Ketua Pengawas": 43, "Pengawas": 494, "Pengemas Bilik": 43, "Sukarelawan": 50},
    "Hulu Langat": {"A-Sekolah Kerajaan": 12659, "B-Sekolah Agensi": 4, "C-Sekolah Bantuan Kerajaan": 32, "D-Sekolah Swasta": 352, "E-Calon Persendirian": 1150, "Penyelia Kawasan": 32, "Ketua Pengawas": 90, "Timbalan Ketua Pengawas": 90, "Pengawas": 1046, "Pengemas Bilik": 90, "Sukarelawan": 45},
    "Gombak": {"A-Sekolah Kerajaan": 9317, "B-Sekolah Agensi": 0, "C-Sekolah Bantuan Kerajaan": 0, "D-Sekolah Swasta": 318, "E-Calon Persendirian": 381, "Penyelia Kawasan": 28, "Ketua Pengawas": 61, "Timbalan Ketua Pengawas": 61, "Pengawas": 845, "Pengemas Bilik": 61, "Sukarelawan": 40},
    "Klang": {"A-Sekolah Kerajaan": 11742, "B-Sekolah Agensi": 0, "C-Sekolah Bantuan Kerajaan": 50, "D-Sekolah Swasta": 941, "E-Calon Persendirian": 791, "Penyelia Kawasan": 30, "Ketua Pengawas": 78, "Timbalan Ketua Pengawas": 78, "Pengawas": 863, "Pengemas Bilik": 78, "Sukarelawan": 48},
    "Kuala Langat": {"A-Sekolah Kerajaan": 4331, "B-Sekolah Agensi": 0, "C-Sekolah Bantuan Kerajaan": 44, "D-Sekolah Swasta": 0, "E-Calon Persendirian": 323, "Penyelia Kawasan": 12, "Ketua Pengawas": 32, "Timbalan Ketua Pengawas": 32, "Pengawas": 358, "Pengemas Bilik": 32, "Sukarelawan": 20},
    "Kuala Selangor": {"A-Sekolah Kerajaan": 4131, "B-Sekolah Agensi": 5, "C-Sekolah Bantuan Kerajaan": 0, "D-Sekolah Swasta": 98, "E-Calon Persendirian": 436, "Penyelia Kawasan": 16, "Ketua Pengawas": 31, "Timbalan Ketua Pengawas": 31, "Pengawas": 389, "Pengemas Bilik": 31, "Sukarelawan": 25},
    "Hulu Selangor": {"A-Sekolah Kerajaan": 3251, "B-Sekolah Agensi": 104, "C-Sekolah Bantuan Kerajaan": 0, "D-Sekolah Swasta": 0, "E-Calon Persendirian": 251, "Penyelia Kawasan": 15, "Ketua Pengawas": 26, "Timbalan Ketua Pengawas": 26, "Pengawas": 240, "Pengemas Bilik": 26, "Sukarelawan": 18},
    "Sabak Bernam": {"A-Sekolah Kerajaan": 1990, "B-Sekolah Agensi": 158, "C-Sekolah Bantuan Kerajaan": 58, "D-Sekolah Swasta": 16, "E-Calon Persendirian": 85, "Penyelia Kawasan": 12, "Ketua Pengawas": 24, "Timbalan Ketua Pengawas": 24, "Pengawas": 197, "Pengemas Bilik": 24, "Sukarelawan": 15},
    "Sepang": {"A-Sekolah Kerajaan": 3477, "B-Sekolah Agensi": 0, "C-Sekolah Bantuan Kerajaan": 48, "D-Sekolah Swasta": 110, "E-Calon Persendirian": 382, "Penyelia Kawasan": 22, "Ketua Pengawas": 28, "Timbalan Ketua Pengawas": 28, "Pengawas": 265, "Pengemas Bilik": 28, "Sukarelawan": 30},
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

# ========== FUNGSI BARU UNTUK DATA CALON - INI KUNCI DIA ==========
FILE_CALON_JSON = "data_calon.json"

def load_data_calon():
    if os.path.exists(FILE_CALON_JSON):
        try:
            with open(FILE_CALON_JSON, "r") as f:
                return json.load(f)
        except:
            return DATA_ASAL
    else:
        return DATA_ASAL

def simpan_data_calon(data):
    with open(FILE_CALON_JSON, "w") as f:
        json.dump(data, f, indent=2)
    st.session_state["data_calon"] = data

#... [fungsi excel yang lain kekal sama]...
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
if "data_calon" not in st.session_state:
    st.session_state["data_calon"] = load_data_calon() # <-- DASHBOARD BACA DARI SINI
if "data_pusat" not in st.session_state: st.session_state["data_pusat"] = load_data_pusat()
if "data_mp" not in st.session_state: st.session_state["data_mp"] = load_data_mp()
if "editor_login" not in st.session_state: st.session_state["editor_login"] = False
if "show_editor" not in st.session_state: st.session_state["show_editor"] = False
if "menu" not in st.session_state: st.session_state["menu"] = "Dashboard"

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
    tab1, tab2, tab3 = st.tabs(["🏫 Selenggara Pusat", "📚 Selenggara Mata Pelajaran", "👥 Selenggara Calon & Petugas"])
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
    with tab3:
        st.subheader("🛠️ Selenggara Bilangan Calon & Petugas - Dashboard Auto Update")
        st.info("Ubah nombor di sini, klik Simpan, Dashboard terus berubah. Data akan disimpan kekal dalam data_calon.json")

        df_edit = pd.DataFrame.from_dict(st.session_state["data_calon"], orient='index')
        st.write("Edit terus dalam jadual:")
        edited_df = st.data_editor(df_edit, use_container_width=True, num_rows="dynamic")

        if st.button("💾 SIMPAN & UPDATE DASHBOARD", type="primary", use_container_width=True):
            data_baru_dict = edited_df.to_dict(orient='index')
            simpan_data_calon(data_baru_dict)
            st.success("Berjaya! Data calon & petugas dah update. Sila lihat Dashboard.")
            st.balloons()
            st.rerun()

def page_cari_mp():
    st.header("📚 Carian Mata Pelajaran Mengikut Pusat")
    df_mp = st.session_state["data_mp"]
    if df_mp.empty: st.warning("Sheet 'MataPelajaran' masih kosong.")
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
                st.dataframe(df_filter[COLUMNS_MP].drop_duplicates(), use_container_width=True)
            else: st.error("⚠️ Tiada pusat yang menawarkan mata pelajaran tersebut")

def page_senarai_pusat():
    st.header("📋 Senarai Pusat Peperiksaan")
    df_pusat = st.session_state["data_pusat"]
    if df_pusat.empty: st.warning("Tiada data pusat.")
    else:
        if st.session_state.get("role") == "PPD": df_pusat = df_pusat[df_pusat["Kod_PPD"] == st.session_state["kod_ppd"]]
        df_output = df_pusat[["Kod_PPD", "No_Pusat", "Nama_Pusat", "Nama_Bilik_Kebal", "Bil_Calon_Pusat"]].sort_values(by=["Kod_PPD", "No_Pusat"])
        st.metric("Jumlah Pusat", len(df_output))
        st.dataframe(df_output, use_container_width=True, hide_index=True)

# ========== HEADER ==========
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

# ========== 2 COLUMN ==========
col_sidebar, col_main = st.columns([1, 4])

with col_sidebar:
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

with col_main:
    if st.session_state["menu"] == "Dashboard":
        data = st.session_state["data_calon"]
        if jenis_data == "Calon": kategori_list = JENIS_CALON[1:] if sub_filter == "Semua Jenis" else [sub_filter]
        elif jenis_data == "Petugas": kategori_list = JENIS_PETUGAS[1:] if sub_filter == "Semua Jawatan" else [sub_filter]
        else: kategori_list = SEMUA_KATEGORI
        jumlah = sum(sum(data[d][k] for k in kategori_list) for d in data) if daerah == "Semua Daerah" else sum(data[daerah][k] for k in kategori_list)
        jumlah_petugas_total = sum(sum(data[d][k] for k in JENIS_PETUGAS[1:]) for d in data)
        jumlah_pusat_total = len(st.session_state["data_pusat"])
        st.info(f"Daerah: **{daerah}** | Data: **{jenis_data}** | Filter: **{sub_filter}**")
        colA, colB, colC = st.columns(3)
        with colA: st.metric(f"Jumlah", f"{jumlah:,}")
        with colB: st.metric("Jumlah Petugas Negeri", f"{jumlah_petugas_total:,}")
        with colC: st.metric("Jumlah Rekod Pusat", f"{jumlah_pusat_total:,}")
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
        LINK_JADUAL_PDF = "https://raw.githubusercontent.com/akashahismail-create/sistem-jpn-selangor/main/Jadual_Waktu_SPM.pdf"
        st.markdown(f"[📥 Klik sini untuk Muat Turun Jadual Waktu]({LINK_JADUAL_PDF})")
        st.markdown(f'<iframe src="{LINK_JADUAL_PDF}" width="100%" height="800" type="application/pdf"></iframe>', unsafe_allow_html=True)
    elif st.session_state["menu"] == "Selenggara": page_selenggara_pusat()
    elif st.session_state["menu"] == "CariMP": page_cari_mp()
    elif st.session_state["menu"] == "SenaraiPusat": page_senarai_pusat()
