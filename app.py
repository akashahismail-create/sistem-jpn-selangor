import streamlit as st
import base64
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from io import BytesIO

st.set_page_config(page_title="JPN Selangor", layout="wide")

hide_st_style = """
    <style>
    #MainMenu {visibility: hidden; height: 0px;}
    footer {visibility: hidden; height: 0px;}
    header {visibility: hidden; height: 0px;}
    div.block-container {
        padding-top: 0rem!important;
        padding-bottom: 0rem!important;
        margin-top: 0rem!important;
    }
    section[data-testid="stMain"] > div:first-child {
        padding-top: 0rem!important;
        margin-top: 0rem!important;
    }
    div[data-testid="stAppViewContainer"] {
        padding-top: 0rem!important;
    }
    section.main > div.block-container > div[data-testid="stVerticalBlock"] > div > div[data-testid="stHorizontalBlock"]:nth-child(1) > div[data-testid="column"]:nth-child(1) > div[data-testid="stVerticalBlock"] {
        background: linear-gradient(180deg, #00695C 0%, #004D40 100%)!important;
        border-radius: 15px!important;
        padding: 15px!important;
        border: 2px solid #FFD700!important;
    }
    button[kind="secondary"] {
        background: linear-gradient(135deg, #00897B 0%, #004D40 100%)!important;
        color: #FFEB3B!important;
        border: 2px solid #FFD700!important;
        border-radius: 10px!important;
        font-weight: bold!important;
    }
    button[kind="secondary"]:hover {
        background: linear-gradient(135deg, #00695C 0%, #004D40 100%)!important;
        color: white!important;
        border-color: white!important;
    }
    button[kind="primary"] {
        background: linear-gradient(135deg, #C62828 0%, #B71C1C 100%)!important;
        border: 2px solid #FFD700!important;
        color: white!important;
        border-radius: 10px!important;
        font-weight: bold!important;
    }
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #00897B 0%, #004D40 100%)!important;
        border: 2px solid #FFD700!important;
        border-radius: 15px!important;
        padding: 20px!important;
        height: 115px!important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2)!important;
    }
    div[data-testid="stMetric"] label {
        color: #FFEB3B!important;
        font-weight: bold!important;
        font-size: 13px!important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #FFEB3B!important;
        font-weight: bold!important;
        font-size: 32px!important;
    }
    div[data-testid="stHorizontalBlock"] { align-items: stretch!important; }
    div[data-testid="stSelectbox"] label p {
        color: black!important; font-weight: 800!important; font-size: 17px!important;
    }
    div[data-baseweb="select"] > div {
        background-color: #004D40!important; border: 2px solid #FFD700!important;
    }
    div[data-baseweb="select"] span {
        color: #FFEB3B!important; font-weight: bold!important; font-size: 16px!important;
    }
    input[data-baseweb="input"] { color: black!important; font-weight: bold!important; }
    div[data-testid="stTextInput"] label p {
        color: black!important; font-weight: 800!important; font-size: 16px!important;
    }
    </style>
    """
st.markdown(hide_st_style, unsafe_allow_html=True)

FILE_NOTIS = "pemberitahuan.json"
DEFAULT_NOTIS = "📢 MAKLUMAN TERKINI: Data Calon SPM 2025 sedang dikemaskini | Sila lengkapkan pengesahan pusat sebelum 30 September 2026 | Sebarang pertanyaan hubungi Sektor Pentaksiran dan Peperiksaan JPN Selangor"
PASSWORD_DELETE = "akashah"

def load_notis():
    if os.path.exists(FILE_NOTIS):
        try:
            with open(FILE_NOTIS, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict) and "teks" in data:
                    return {"teks": data.get("teks", DEFAULT_NOTIS), "image": data.get("image")}
                else:
                    return {"teks": DEFAULT_NOTIS, "image": None}
        except:
            return {"teks": DEFAULT_NOTIS, "image": None}
    else:
        return {"teks": DEFAULT_NOTIS, "image": None}

def simpan_notis(teks, image_b64=None):
    with open(FILE_NOTIS, "w", encoding="utf-8") as f:
        json.dump({"teks": teks, "image": image_b64, "dikemaskini": datetime.now().strftime("%Y-%m-%d %H:%M")}, f, ensure_ascii=False, indent=2)

data_notis = load_notis()
teks_notis = data_notis.get("teks","")
img_notis = data_notis.get("image")
if teks_notis.strip()!="" or img_notis:
    img_tag = f'<img src="data:image/png;base64,{img_notis}" style="height:28px; vertical-align:middle; margin-right:12px; border:1px solid #FFD700; border-radius:4px; background:white;">' if img_notis else ""
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, #B71C1C 0%, #C62828 100%); border: 2px solid #FFD700; border-radius: 10px; padding: 8px 0px; margin-bottom: 12px; box-shadow: 0 3px 8px rgba(0,0,0,0.2);">
        <marquee behavior="scroll" direction="left" scrollamount="7" style="color: #FFEB3B; font-weight: bold; font-size: 15px; font-family: sans-serif;">
            {img_tag} {teks_notis} &nbsp;&nbsp;&nbsp; • &nbsp;&nbsp;&nbsp; {teks_notis}
        </marquee>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='text-align: right; font-size: 10px; color: grey;'>Created by: Akashah Ismail</div>", unsafe_allow_html=True)

if 'menu_state' not in st.session_state: st.session_state.menu_state = True

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
KOD_PPD = {"Petaling Perdana": "BH", "Petaling Utama": "BK", "Hulu Langat": "BD", "Gombak": "BG", "Klang": "BA", "Kuala Langat": "BB", "Kuala Selangor": "BC", "Hulu Selangor": "BE", "Sabak Bernam": "BF", "Sepang": "BJ"}
USERS = {
    "admin": {"password": "jpn", "role": "Admin", "tahap": "JPN"},
    "bh": {"password": "bh", "role": "PPD", "daerah": "Petaling Perdana"},
    "bk": {"password": "bk", "role": "PPD", "daerah": "Petaling Utama"},
    "bd": {"password": "bd", "role": "PPD", "daerah": "Hulu Langat"},
    "bg": {"password": "bg", "role": "PPD", "daerah": "Gombak"},
    "ba": {"password": "ba", "role": "PPD", "daerah": "Klang"},
    "bb": {"password": "bb", "role": "PPD", "daerah": "Kuala Langat"},
    "bc": {"password": "bc", "role": "PPD", "daerah": "Kuala Selangor"},
    "be": {"password": "be", "role": "PPD", "daerah": "Hulu Selangor"},
    "bf": {"password": "bf", "role": "PPD", "daerah": "Sabak Bernam"},
    "bj": {"password": "bj", "role": "PPD", "daerah": "Sepang"},
}
FILE_EXCEL = "data_v1.1.xlsx"
SHEET_PUSAT = "selenggara_pusat"
SHEET_MP = "MataPelajaran"
COLUMNS_PUSAT = ["Kod_PPD","No_Pusat","Nama_Pusat","Bil_Calon_Pusat","Nama_Bilik_Kebal","Dikemaskini_Oleh","Tarikh_Kemaskini"]
COLUMNS_MP = ["Kod_PPD","No_Pusat","Nama_Pusat","KodMP","NamaMP","Kertas","Tarikh"]
LINK_PENGURUSAN = "https://drive.google.com/drive/folders/193ELWVyPDORTVE7ZSVe2B3rsZILkg7f6?usp=drive_link"
FILE_CALON_JSON = "data_calon.json"

def load_data_calon():
    if os.path.exists(FILE_CALON_JSON):
        try:
            with open(FILE_CALON_JSON, "r") as f: return json.load(f)
        except: return DATA_ASAL
    else: return DATA_ASAL
def simpan_data_calon(data):
    with open(FILE_CALON_JSON, "w") as f: json.dump(data, f, indent=2)
    st.session_state["data_calon"] = data
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

if "data_calon" not in st.session_state: st.session_state["data_calon"] = load_data_calon()
if "data_pusat" not in st.session_state: st.session_state["data_pusat"] = load_data_pusat()
if "data_mp" not in st.session_state: st.session_state["data_mp"] = load_data_mp()
if "editor_login" not in st.session_state: st.session_state["editor_login"] = False
if "show_editor" not in st.session_state: st.session_state["show_editor"] = False
if "menu" not in st.session_state: st.session_state["menu"] = "Dashboard"

def login_editor():
    with st.form("login_form"):
        st.markdown("#### 🔒 Log Masuk")
        username = st.text_input("Nama Pengguna", key="user_login", placeholder="Masukkan nama pengguna")
        password = st.text_input("Kata Laluan", type="password", key="pass_login", placeholder="Masukkan kata laluan")
        submitted = st.form_submit_button("Log Masuk", use_container_width=True, type="primary")
        if submitted:
            uname = username.lower().strip()
            if uname in USERS and USERS[uname]["password"] == password:
                st.session_state["editor_login"] = True
                st.session_state["username"] = uname
                st.session_state["role"] = USERS[uname]["role"]
                if USERS[uname]["role"] == "PPD":
                    st.session_state["daerah_ppd"] = USERS[uname]["daerah"]
                    st.session_state["kod_ppd"] = KOD_PPD[USERS[uname]["daerah"]]
                st.success(f"Berjaya login sebagai {uname}!"); st.rerun()
            else: st.error("Nama pengguna atau kata laluan salah!")

def page_selenggara_pusat():
    st.header("⚙️ Selenggara Data")
    if not st.session_state.get("editor_login", False):
        st.warning("Sila login dahulu di menu Selenggara Data"); return
    role = st.session_state.get("role", "")

    if role == "Admin":
        tab_pusat, tab_mp, tab_calon, tab_notis, tab_db = st.tabs(["🏫 Selenggara Pusat", "📚 Selenggara Mata Pelajaran", "👥 Selenggara Calon & Petugas", "📢 Pemberitahuan Atas", "💾 Urus File v1.1"])
    else:
        tab_pusat, tab_calon = st.tabs(["🏫 Selenggara Pusat", "👥 Selenggara Calon & Petugas"])
        tab_mp = None
        tab_notis = None
        tab_db = None

    with tab_pusat:
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
        else:
            pilihan_ppd = st.session_state["kod_ppd"]
            st.info(f"Anda login sebagai PPD: {st.session_state['daerah_ppd']} - {pilihan_ppd}")
        with st.form("form_pusat"):
            col1, col2 = st.columns(2)
            with col1:
                no_pusat = st.text_input("No Pusat *")
                nama_pusat = st.text_input("Nama Pusat *")
            with col2:
                bil_calon = st.number_input("Bilangan Calon Ikut Pusat", min_value=0, step=1)
                nama_kebal = st.text_input("Nama Bilik Kebal")
            submitted = st.form_submit_button("💾 Simpan Data", type="primary", use_container_width=True)
            if submitted:
                if no_pusat == "" or nama_pusat == "": st.error("No Pusat dan Nama Pusat wajib diisi")
                else:
                    simpan_data_pusat(pilihan_ppd, no_pusat, nama_pusat, bil_calon, nama_kebal, st.session_state["username"])
                    st.success("Data berjaya disimpan!"); st.rerun()
        st.write("---")
        st.subheader(f"Senarai Pusat di {pilihan_ppd} - Klik Terus Untuk Edit Ejaan")
        st.info("💡 Double-click pada Nama_Pusat untuk betulkan ejaan. Lepas edit, tekan SIMPAN.")
        df_tunjuk = st.session_state["data_pusat"][st.session_state["data_pusat"]['Kod_PPD'] == pilihan_ppd]
        if df_tunjuk.empty:
            st.warning("Tiada data lagi untuk PPD ini.")
            edited_df = pd.DataFrame(columns=COLUMNS_PUSAT)
        else:
            edited_df = st.data_editor(
                df_tunjuk, use_container_width=True, num_rows="dynamic",
                key=f"editor_pusat_{pilihan_ppd}",
                column_config={
                    "Kod_PPD": st.column_config.TextColumn("Kod_PPD", disabled=True, width="small"),
                    "No_Pusat": st.column_config.TextColumn("No_Pusat", width="small"),
                    "Nama_Pusat": st.column_config.TextColumn("Nama_Pusat", width="large"),
                    "Bil_Calon_Pusat": st.column_config.TextColumn("Bil Calon"),
                    "Nama_Bilik_Kebal": st.column_config.TextColumn("Bilik Kebal"),
                    "Dikemaskini_Oleh": st.column_config.TextColumn("Oleh", disabled=True),
                    "Tarikh_Kemaskini": st.column_config.TextColumn("Tarikh", disabled=True),
                }
            )
        if st.button("💾 SIMPAN PERUBAHAN EJAAN / EDIT TERUS", type="primary", use_container_width=True):
            if not edited_df.empty:
                edited_df['Dikemaskini_Oleh'] = st.session_state["username"]
                edited_df['Tarikh_Kemaskini'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                df_lain = st.session_state["data_pusat"][st.session_state["data_pusat"]['Kod_PPD']!= pilihan_ppd]
                st.session_state["data_pusat"] = pd.concat([df_lain, edited_df], ignore_index=True)
                simpan_ke_excel()
                st.success(f"Berjaya! {len(edited_df)} rekod {pilihan_ppd} dikemaskini."); st.rerun()

    if role == "Admin" and tab_mp is not None:
        with tab_mp:
            st.subheader("📚 Selenggara Mata Pelajaran - ADMIN SAHAJA")
            st.error("🔒 Hanya Admin (jpn) boleh upload / update Mata Pelajaran. PPD tidak dibenarkan.")
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

    with tab_calon:
        st.subheader("🛠️ Selenggara Bilangan Calon & Petugas")
        df_edit = pd.DataFrame.from_dict(st.session_state["data_calon"], orient='index')
        edited_df2 = st.data_editor(df_edit, use_container_width=True, num_rows="dynamic")
        if st.button("💾 SIMPAN & UPDATE DASHBOARD", type="primary", use_container_width=True):
            data_baru_dict = edited_df2.to_dict(orient='index')
            simpan_data_calon(data_baru_dict)
            st.success("Berjaya! Dashboard dah guna data baru."); st.balloons(); st.rerun()

    if role == "Admin" and tab_notis is not None:
        with tab_notis:
            st.subheader("📢 Selenggara Pemberitahuan Berjalan Atas - ADMIN SAHAJA")
            st.error("🔒 Hanya Admin boleh edit bahagian ini.")
            data_n = load_notis()
            current_notis = data_n.get("teks","")
            current_img = data_n.get("image")
            teks_baru = st.text_area("Teks Pemberitahuan:", value=current_notis, height=120)
            st.write("**Muat Naik Imej PNG/JPG (pilihan):**")
            up_img = st.file_uploader("Pilih fail PNG/JPG", type=["png","jpg","jpeg"], key="up_notis_img")
            if up_img:
                st.image(up_img, width=250, caption="Preview Imej Baru")
            elif current_img:
                st.image(base64.b64decode(current_img), width=250, caption="Imej Sedia Ada")
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                if st.button("💾 Simpan Pemberitahuan", type="primary", use_container_width=True):
                    final_b64 = current_img
                    if up_img:
                        final_b64 = base64.b64encode(up_img.getvalue()).decode()
                    simpan_notis(teks_baru, final_b64)
                    st.success("Berjaya dikemaskini!"); st.rerun()
            with col_s2:
                if st.button("🗑️ Padam Semua", use_container_width=True):
                    simpan_notis("", None); st.success("Dipadam."); st.rerun()
            with col_s3:
                if st.button("❌ Buang Imej Sahaja", use_container_width=True):
                    simpan_notis(current_notis, None); st.success("Imej dibuang."); st.rerun()

    if role == "Admin" and tab_db is not None:
        with tab_db:
            st.subheader("💾 Urus File Database data_v1.1.xlsx")
            st.caption("Hanya Admin. Password delete tersembunyi.")
            if os.path.exists(FILE_EXCEL):
                saiz = os.path.getsize(FILE_EXCEL) / 1024
                tarikh = datetime.fromtimestamp(os.path.getmtime(FILE_EXCEL)).strftime("%Y-%m-%d %H:%M:%S")
                st.success(f"✅ File WUJUD | {FILE_EXCEL} | {saiz:.1f} KB | {tarikh}")
                with open(FILE_EXCEL, "rb") as f:
                    st.download_button("📥 Download Backup File Lama Dulu (Wajib)", f.read(), FILE_EXCEL, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
                st.write("---")
                st.error("⚠️ ZON BAHAYA - Delete Perlukan Password")
                c1, c2 = st.columns(2)
                with c1:
                    confirm = st.checkbox("Saya faham & nak delete", key="confirm_del")
                with c2:
                    pwd_del = st.text_input("Password Delete:", type="password", placeholder="Masukkan password", key="pwd_del")
                boleh_delete = confirm and (pwd_del == PASSWORD_DELETE)
                if confirm and pwd_del!= "" and pwd_del!= PASSWORD_DELETE:
                    st.warning("❌ Password salah!")
                elif boleh_delete:
                    st.success("✅ Password betul, boleh delete")
                if st.button("🗑️ DELETE FILE LAMA SEKARANG", type="primary", use_container_width=True, disabled=not boleh_delete):
                    try:
                        os.remove(FILE_EXCEL)
                        st.session_state["data_pusat"] = pd.DataFrame(columns=COLUMNS_PUSAT)
                        st.session_state["data_mp"] = pd.DataFrame(columns=COLUMNS_MP)
                        st.success(f"File {FILE_EXCEL} berjaya dipadam! Sekarang upload file baru di bawah.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Gagal delete: {e}")
            else:
                st.warning(f"❌ File {FILE_EXCEL} TIADA dalam folder. Sila upload file baru di bawah.")

            st.write("---")
            st.subheader("📤 Upload File Baru Ganti Yang Lama")
            up_new = st.file_uploader(f"Pilih file {FILE_EXCEL} yang baru", type=["xlsx"], key="up_new_db")
            if up_new is not None:
                st.info(f"File dipilih: {up_new.name} | {up_new.size/1024:.1f} KB")
                try:
                    xls = pd.ExcelFile(up_new, engine='openpyxl')
                    st.write(f"Sheet dalam file: {xls.sheet_names}")
                    if SHEET_PUSAT in xls.sheet_names:
                        df_prev = pd.read_excel(xls, sheet_name=SHEET_PUSAT, engine='openpyxl')
                        st.write(f"Preview {SHEET_PUSAT}: {len(df_prev)} rekod")
                        st.dataframe(df_prev.head(3), use_container_width=True)
                except Exception as e:
                    st.error(f"Ralat baca: {e}")
                if st.button("✅ SAHKAN & GANTI FILE V1.1 DENGAN FILE BARU", type="primary", use_container_width=True):
                    try:
                        with open(FILE_EXCEL, "wb") as f:
                            f.write(up_new.getbuffer())
                        st.session_state["data_pusat"] = load_data_pusat()
                        st.session_state["data_mp"] = load_data_mp()
                        st.success(f"✅ Berjaya ganti! Pusat: {len(st.session_state['data_pusat'])} | MP: {len(st.session_state['data_mp'])}")
                        st.balloons(); st.rerun()
                    except Exception as e:
                        st.error(f"Gagal upload: {e}")

            # === BUTTON BARU BUKA GITHUB + PASSWORD ===
            st.write("---")
            st.subheader("🔗 Buka Github Repository")
            st.caption("Perlu password akashah juga untuk buka link Github")
            pwd_github = st.text_input("Password Github:", type="password", placeholder="Masukkan password", key="pwd_github")
            boleh_github = (pwd_github == PASSWORD_DELETE)
            if pwd_github != "" and not boleh_github:
                st.warning("❌ Password Github salah!")
            elif boleh_github:
                st.success("✅ Password betul, boleh buka Github")
            
            # Link Github cikgu
            LINK_GITHUB = "https://github.com/akashahismail-create/sistem-jpn-selangor"
            if st.button("🌐 BUKA GITHUB SEKARANG", use_container_width=True, disabled=not boleh_github):
                st.markdown(f'<meta http-equiv="refresh" content="0; url={LINK_GITHUB}">', unsafe_allow_html=True)
                st.link_button(f"➡️ Klik sini jika tak auto buka: {LINK_GITHUB}", LINK_GITHUB, use_container_width=True, type="primary")  
def page_cari_mp():
    st.header("📚 Carian Mata Pelajaran Mengikut Pusat")
    df_mp = st.session_state["data_mp"]
    if df_mp.empty: st.warning("Sheet 'MataPelajaran' masih kosong.")
    else:
        col1, col2, col3, col4 = st.columns([2,2,1,2])
        with col1: cari_kod = st.text_input("1. Masukkan Kod Mata Pelajaran", placeholder="Contoh: 1103")
        with col2: cari_nama = st.text_input("2. ATAU Nama Mata Pelajaran", placeholder="Contoh: MATEMATIK")
        with col3: cari_kertas = st.selectbox("3. Pilih Kertas", ["Semua", "1", "2", "3"])
        with col4: cari_daerah = st.selectbox("4. Pilih Daerah", ["Semua Daerah"] + list(KOD_PPD.keys()))
        if st.button("🔍 Cari Sekarang", type="primary", use_container_width=True):
            df_filter = df_mp.copy()
            if st.session_state.get("role") == "PPD": df_filter = df_filter[df_filter["Kod_PPD"] == st.session_state["kod_ppd"]]
            else:
                if cari_daerah!= "Semua Daerah":
                    kod_ppd_pilihan = KOD_PPD[cari_daerah]
                    df_filter = df_filter[df_filter["Kod_PPD"] == kod_ppd_pilihan]
            if cari_kod: df_filter = df_filter[df_filter["KodMP"].str.contains(cari_kod, case=False, na=False)]
            elif cari_nama: df_filter = df_filter[df_filter["NamaMP"].str.contains(cari_nama, case=False, na=False)]
            if cari_kertas!= "Semua": df_filter = df_filter[df_filter["Kertas"].astype(str) == cari_kertas]
            if not df_filter.empty:
                jumlah_rekod = len(df_filter)
                jumlah_pusat_unik = df_filter.drop_duplicates(subset=["Kod_PPD", "No_Pusat"]).shape[0]
                st.success(f"✅ Jumpa {jumlah_rekod} rekod")
                m1, m2 = st.columns(2)
                with m1: st.metric("Jumlah Rekod MP", f"{jumlah_rekod:,}")
                with m2: st.metric(f"Jumlah Pusat Tawar {cari_kod if cari_kod else cari_nama if cari_nama else 'MP'}", f"{jumlah_pusat_unik:,} pusat")
                st.dataframe(df_filter[COLUMNS_MP].drop_duplicates(), use_container_width=True)
            else: st.error("⚠️ Tiada pusat yang menawarkan mata pelajaran tersebut")

def page_senarai_pusat():
    st.header("📋 Senarai Pusat Peperiksaan")
    df_pusat = st.session_state["data_pusat"]
    if df_pusat.empty: st.warning("Tiada data pusat. Sila upload di Selenggara Data.")
    else:
        if st.session_state.get("role") == "PPD":
            kod_ppd_user = st.session_state["kod_ppd"]
            daerah_user = st.session_state["daerah_ppd"]
            df_tapis = df_pusat[df_pusat["Kod_PPD"] == kod_ppd_user]
            st.markdown(f"<div style='background:linear-gradient(135deg,#00897B 0%,#004D40 100%); border:2px solid #FFD700; border-radius:12px; padding:12px 15px; color:#FFEB3B; font-weight:bold; font-size:16px;'>📍 Daerah anda: {daerah_user} ({kod_ppd_user}) | Jumlah Pusat: {len(df_tapis):,}</div>", unsafe_allow_html=True)
            st.write(""); st.metric(f"Jumlah Pusat {daerah_user}", f"{len(df_tapis):,}")
            df_output = df_tapis[["Kod_PPD", "No_Pusat", "Nama_Pusat", "Nama_Bilik_Kebal", "Bil_Calon_Pusat"]].sort_values(by=["Kod_PPD", "No_Pusat"])
            st.dataframe(df_output, use_container_width=True, hide_index=True)
        else:
            col1, col2 = st.columns([2, 3])
            with col1: pilih_daerah_pusat = st.selectbox("📍 Pilih Daerah:", ["Semua Daerah"] + list(KOD_PPD.keys()), key="filter_pusat_daerah")
            if pilih_daerah_pusat == "Semua Daerah":
                df_tapis = df_pusat
                st.markdown(f"<div style='background:linear-gradient(135deg,#00897B 0%,#004D40 100%); border:2px solid #FFD700; border-radius:12px; padding:12px 15px; color:#FFEB3B; font-weight:bold; font-size:16px;'>📍 Memaparkan keseluruhan Selangor | Jumlah Pusat Keseluruhan: {len(df_tapis):,}</div>", unsafe_allow_html=True)
                st.write("")
                c1, c2 = st.columns(2)
                with c1: st.metric("Jumlah Pusat Keseluruhan", f"{len(df_tapis):,}")
                with c2: st.metric("Jumlah Daerah", f"{len(KOD_PPD)} daerah")
            else:
                kod_filter = KOD_PPD[pilih_daerah_pusat]
                df_tapis = df_pusat[df_pusat["Kod_PPD"] == kod_filter]
                st.markdown(f"<div style='background:linear-gradient(135deg,#00897B 0%,#004D40 100%); border:2px solid #FFD700; border-radius:12px; padding:12px 15px; color:#FFEB3B; font-weight:bold; font-size:16px;'>📍 Daerah: {pilih_daerah_pusat} ({kod_filter}) | Jumlah Pusat {pilih_daerah_pusat}: {len(df_tapis):,}</div>", unsafe_allow_html=True)
                st.write(""); st.metric(f"Jumlah Pusat {pilih_daerah_pusat}", f"{len(df_tapis):,}")
            carian = st.text_input("🔍 Cari Nama Pusat / No Pusat:", placeholder="Contoh: SMK Klang atau BA 145")
            if carian: df_tapis = df_tapis[df_tapis["Nama_Pusat"].str.contains(carian, case=False, na=False) | df_tapis["No_Pusat"].str.contains(carian, case=False, na=False)]
            df_output = df_tapis[["Kod_PPD", "No_Pusat", "Nama_Pusat", "Nama_Bilik_Kebal", "Bil_Calon_Pusat"]].sort_values(by=["Kod_PPD", "No_Pusat"])
            st.dataframe(df_output, use_container_width=True, hide_index=True)
            st.download_button("📥 Download Senarai Pusat (Excel)", to_excel(df_output), f"senarai_pusat_{pilih_daerah_pusat}.xlsx", use_container_width=True)

if os.path.exists("logo.png"):
    with open("logo.png", "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode()
        logo_html = f'<img src="data:image/png;base64,{logo_b64}" width="110" style="border:2px solid #FFD700; border-radius:10px;">'
else: logo_html = '<div style="font-size:50px;">🏛️</div>'

st.markdown(f"""
<div style="background: linear-gradient(90deg, #004D40 0%, #00695C 100%); border: 2px solid #FFD700; border-radius: 15px; padding: 15px 20px; margin-bottom: 15px;">
    <div style="display: flex; align-items: center;">
        <div style="margin-right: 20px;">{logo_html}</div>
        <div>
            <div style="color: #FFD700; font-size: 26px; font-weight: bold;">JABATAN PENDIDIKAN SELANGOR</div>
            <div style="color: white; font-size: 18px;">SEKTOR PENTAKSIRAN DAN PEPERIKSAAN</div>
            <div style="color: #FFD700; margin-top: 8px; border-top: 1px solid #FFD700; padding-top: 5px; font-weight: bold;">SIJIL PELAJARAN MALAYSIA</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

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
    st.markdown("""<a href="https://sppat.moe.gov.my" target="_blank" style="display:block; text-align:center; background:linear-gradient(135deg, #00897B 0%, #004D40 100%); border:2px solid #FFD700; color:#FFEB3B; padding:10px; border-radius:10px; text-decoration:none; font-weight:bold; margin-bottom:10px;">1. SPPAT</a>""", unsafe_allow_html=True)
    st.markdown("""<a href="https://elp.moe.gov.my/eportal/login" target="_blank" style="display:block; text-align:center; background:linear-gradient(135deg, #00897B 0%, #004D40 100%); border:2px solid #FFD700; color:#FFEB3B; padding:10px; border-radius:10px; text-decoration:none; font-weight:bold; margin-bottom:10px;">2. ELP Portal</a>""", unsafe_allow_html=True)
    if st.session_state.get("editor_login", False):
        st.link_button("3. Selenggara Calon PPD", "https://script.google.com/macros/s/AKfycbwav3jbWQEkTW2yTK9PnanlItxPM5NpCHADLNb_BRjY4hmsale257tSqMsRTdqv88HA/exec", use_container_width=True, type="primary")
        st.write("---")
        st.markdown("### 📁 Pautan Pengurusan")
        st.link_button("4. Pengurusan", LINK_PENGURUSAN, use_container_width=True, type="primary")
        st.link_button("5. Sistem IPEP Selangor", "http://ipep.my/selangor/", use_container_width=True, type="primary")
    st.write("---")
    if st.session_state.get("editor_login", False):
        if st.button("🛠️ Selenggara Pusat", use_container_width=True, type="primary"): st.session_state["menu"] = "Selenggara"; st.rerun()
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
        if daerah == "Semua Daerah":
            jumlah_calon_total = sum(sum(data[d][k] for k in JENIS_CALON[1:]) for d in data)
            jumlah_petugas_total = sum(sum(data[d][k] for k in JENIS_PETUGAS[1:]) for d in data)
            jumlah_pusat_total = sum(data[d]["Ketua Pengawas"] for d in data)
        else:
            jumlah_calon_total = sum(data[daerah][k] for k in JENIS_CALON[1:])
            jumlah_petugas_total = sum(data[daerah][k] for k in JENIS_PETUGAS[1:])
            jumlah_pusat_total = data[daerah]["Ketua Pengawas"]
        if daerah == "Semua Daerah": st.info(f"📍 Memaparkan **keseluruhan Selangor** | Calon: **{jumlah_calon_total:,}** | Petugas: **{jumlah_petugas_total:,}** | Pusat: **{jumlah_pusat_total:,}**")
        else: st.info(f"📍 Daerah: **{daerah}** | Calon {daerah}: **{jumlah_calon_total:,}** | Petugas {daerah}: **{jumlah_petugas_total:,}** | Pusat {daerah}: **{jumlah_pusat_total:,}** | Filter: **{jenis_data} - {sub_filter}**")
        colA, colB, colC = st.columns(3)
        with colA:
            if daerah == "Semua Daerah": st.metric("Jumlah Calon Keseluruhan", f"{jumlah_calon_total:,}")
            else: st.metric(f"Jumlah Calon {daerah}", f"{jumlah_calon_total:,}")
        with colB:
            if daerah == "Semua Daerah": st.metric("Jumlah Petugas Keseluruhan", f"{jumlah_petugas_total:,}")
            else: st.metric(f"Jumlah Petugas {daerah}", f"{jumlah_petugas_total:,}")
        with colC:
            if daerah == "Semua Daerah": st.metric("Jumlah Pusat Keseluruhan", f"{jumlah_pusat_total:,}")
            else: st.metric(f"Jumlah Pusat {daerah}", f"{jumlah_pusat_total:,}")
        st.write("---")
        if jenis_data == "Calon" or jenis_data == "Semua":
            st.subheader("📊 Bilangan Calon Mengikut Daerah")
            df_calon = pd.DataFrame([{k: v[k] for k in JENIS_CALON[1:]} for v in data.values()], index=data.keys())
            if daerah!= "Semua Daerah": df_calon = df_calon.loc[[daerah]]
            if sub_filter!= "Semua Jenis" and jenis_data == "Calon": df_calon = df_calon[[sub_filter]]
            st.dataframe(df_calon, use_container_width=True)
            fig1, ax1 = plt.subplots(figsize=(11, 5.5))
            df_calon.plot(kind='bar', ax=ax1, width=0.8)
            ax1.set_ylabel("Bilangan Calon", fontweight='bold', fontsize=12, color='black')
            ax1.set_xlabel("Daerah", fontweight='bold', fontsize=12, color='black')
            ax1.tick_params(axis='x', labelsize=10, colors='black')
            ax1.tick_params(axis='y', labelsize=11, colors='black')
            for label in ax1.get_xticklabels(): label.set_fontweight('bold'); label.set_color('black'); label.set_rotation(45); label.set_ha('right')
            leg = ax1.legend(title="Jenis Calon", bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
            plt.setp(leg.get_texts(), color='black', fontweight='bold'); plt.setp(leg.get_title(), color='black', fontweight='bold')
            for container in ax1.containers:
                labels = [f"{int(v)}" if v > 300 else "" for v in container.datavalues]
                ax1.bar_label(container, labels=labels, label_type='edge', fontsize=10, fontweight='bold', color='black', padding=4)
            plt.tight_layout(); st.pyplot(fig1)
        if jenis_data == "Petugas" or jenis_data == "Semua":
            st.write("---")
            st.subheader("👮 Bilangan Petugas Mengikut Daerah")
            df_petugas = pd.DataFrame([{k: v[k] for k in JENIS_PETUGAS[1:]} for v in data.values()], index=data.keys())
            if daerah!= "Semua Daerah": df_petugas = df_petugas.loc[[daerah]]
            if sub_filter!= "Semua Jawatan" and jenis_data == "Petugas": df_petugas = df_petugas[[sub_filter]]
            st.dataframe(df_petugas, use_container_width=True)
            fig2, ax2 = plt.subplots(figsize=(11, 5.5))
            df_petugas.plot(kind='bar', ax=ax2, width=0.8)
            ax2.set_ylabel("Bilangan Petugas", fontweight='bold', fontsize=12, color='black')
            ax2.set_xlabel("Daerah", fontweight='bold', fontsize=12, color='black')
            ax2.tick_params(axis='x', labelsize=10, colors='black')
            ax2.tick_params(axis='y', labelsize=11, colors='black')
            for label in ax2.get_xticklabels(): label.set_fontweight('bold'); label.set_color('black'); label.set_rotation(45); label.set_ha('right')
            leg2 = ax2.legend(title="Jawatan Petugas", bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
            plt.setp(leg2.get_texts(), color='black', fontweight='bold'); plt.setp(leg2.get_title(), color='black', fontweight='bold')
            for container in ax2.containers:
                labels = [f"{int(v)}" if v > 20 else "" for v in container.datavalues]
                ax2.bar_label(container, labels=labels, label_type='edge', fontsize=10, fontweight='bold', color='black', padding=4)
            plt.tight_layout(); st.pyplot(fig2)
    elif st.session_state["menu"] == "Jadual":
        st.subheader("📅 Jadual Waktu SPM")
        LINK_JADUAL_PDF = "https://raw.githubusercontent.com/akashahismail-create/sistem-jpn-selangor/main/Jadual_Waktu_SPM.pdf"
        st.markdown(f"[📥 Klik sini untuk Muat Turun Jadual Waktu]({LINK_JADUAL_PDF})")
        st.markdown(f'<iframe src="{LINK_JADUAL_PDF}" width="100%" height="800" type="application/pdf"></iframe>', unsafe_allow_html=True)
    elif st.session_state["menu"] == "Selenggara": page_selenggara_pusat()
    elif st.session_state["menu"] == "CariMP": page_cari_mp()
    elif st.session_state["menu"] == "SenaraiPusat": page_senarai_pusat()
