# ==============================================================================
# SISTEM JPN SELANGOR - app_9_v10 - Versi Runnable + Berkomen Penuh
# Created by: Akashah Ismail (Kashah) | Dibantu oleh: Aira
# Tarikh: SPM 2026 | File ini BOLEH RUN terus: streamlit run app_9_v10_commented_runnable.py
# Setiap bahagian ada komen # [KATEGORI] untuk rujukan
# ==============================================================================

import streamlit as st
import base64
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    px = None
    go = None
from datetime import datetime
from io import BytesIO

# [CONFIG] Set tajuk tab & layout wide supaya full width
st.set_page_config(page_title="JPN Selangor SPM 2026", layout="wide", page_icon="🏛️")

# ===== V28 SUPER CANTIK SPM 2026 - DARK MODE STATE =====
if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = False
if "filter_daerah_v14" not in st.session_state:
    st.session_state["filter_daerah_v14"] = "Semua Daerah"

# Koordinat pusat daerah Selangor untuk peta interaktif
DAERAH_COORDS = {
    "Petaling Perdana": {"lat": 3.0733, "lon": 101.5185},
    "Petaling Utama": {"lat": 3.1123, "lon": 101.6051},
    "Klang": {"lat": 3.0333, "lon": 101.45},
    "Gombak": {"lat": 3.2361, "lon": 101.6482},
    "Hulu Langat": {"lat": 3.0738, "lon": 101.7833},
    "Sepang": {"lat": 2.8091, "lon": 101.7167},
    "Kuala Langat": {"lat": 2.8167, "lon": 101.5},
    "Kuala Selangor": {"lat": 3.35, "lon": 101.25},
    "Hulu Selangor": {"lat": 3.5667, "lon": 101.65},
    "Sabak Bernam": {"lat": 3.7667, "lon": 101.0},
}

# [KEEP ALIVE - PART 2] Elak Streamlit sleep + bantu UptimeRobot
# Kod ini tidak ganggu user, cuma tambah 'heartbeat' senyap di background
try:
    from streamlit_autorefresh import st_autorefresh
    # Refresh senyap setiap 25 minit (1500000 ms) untuk elak idle timeout
    st_autorefresh(interval=1500000, key="keepalive_jpn")
except:
    # Kalau library tak ada, guna meta refresh 30 minit sebagai backup
    # User tak perasan pun, page cuma refresh bila dah 30 min idle
    st.markdown('<meta http-equiv="refresh" content="1800">', unsafe_allow_html=True)



# SUPER UI V28 - SPM 2026 - HERO + GLASS + GLOW
dark_bg = "#121212" if st.session_state.get("dark_mode", False) else "#FAFAFA"
filter_bg = "#1E3A3A" if st.session_state.get("dark_mode", False) else "#FFFFFF"
filter_text = "#FFEB3B" if st.session_state.get("dark_mode", False) else "#004D40"
filter_border = "#FFD700"
is_dark = st.session_state.get("dark_mode", False)
hide_st_style = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&display=swap');
    #MainMenu {{visibility: hidden; height: 0px;}}
    footer {{visibility: hidden; height: 0px;}}
    header {{visibility: hidden; height: 0px;}}
    div.block-container {{
        padding-top: 0.5rem!important;
        background: {dark_bg}!important;
    }}
    section.main > div.block-container > div[data-testid="stVerticalBlock"] > div > div[data-testid="stHorizontalBlock"]:nth-child(1) > div[data-testid="column"]:nth-child(1) > div[data-testid="stVerticalBlock"] {{
        background: linear-gradient(180deg, #00695C 0%, #004D40 100%)!important;
        border-radius: 16px!important;
        padding: 16px!important;
        border: 2px solid #FFD700!important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3)!important;
    }}
    /* HERO BANNER SHIMMER + COUNTDOWN BERKELIP KELIP V42 */
    @keyframes blinkGold {{
        0% {{ box-shadow: 0 0 15px rgba(255,215,0,0.6), 0 0 30px rgba(255,215,0,0.3); border-color: #FFD700; transform: scale(1); }}
        50% {{ box-shadow: 0 0 25px rgba(255,215,0,1), 0 0 45px rgba(255,215,0,0.6); border-color: #FFEB3B; transform: scale(1.05); }}
        100% {{ box-shadow: 0 0 15px rgba(255,215,0,0.6), 0 0 30px rgba(255,215,0,0.3); border-color: #FFD700; transform: scale(1); }}
    }}
    @keyframes numberPulse {{
        0% {{ color: white; text-shadow: 0 2px 8px rgba(0,0,0,0.5); transform: scale(1); }}
        50% {{ color: #FFEB3B; text-shadow: 0 0 15px rgba(255,235,59,0.9), 0 0 25px rgba(255,215,0,0.7); transform: scale(1.15); }}
        100% {{ color: white; text-shadow: 0 2px 8px rgba(0,0,0,0.5); transform: scale(1); }}
    }}
    @keyframes textBlink {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.6; }}
    }}
    .countdown-box {{
        animation: blinkGold 1.5s infinite ease-in-out;
    }}
    .countdown-number {{
        animation: numberPulse 1.5s infinite ease-in-out;
    }}
    .countdown-label {{
        animation: textBlink 1s infinite ease-in-out;
    }}

    /* HERO BANNER SHIMMER */
    .hero-banner {{
        background: linear-gradient(135deg, #004D40 0%, #00695C 25%, #00897B 50%, #00695C 75%, #004D40 100%);
        border: 3px solid #FFD700;
        border-radius: 20px;
        padding: 20px 28px;
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0,0,0,0.35), 0 0 25px rgba(255,215,0,0.25);
    }}
    .hero-banner::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,215,0,0.35), transparent);
        animation: shimmer 3.2s infinite;
    }}
    @keyframes shimmer {{
        0% {{left: -100%;}}
        100% {{left: 100%;}}
    }}
    .hero-title {{
        color: #FFD700;
        font-size: 28px;
        font-weight: 800;
        font-family: 'Poppins', sans-serif;
        letter-spacing: 1px;
        text-shadow: 0 2px 12px rgba(255,215,0,0.6);
    }}
    .hero-subtitle {{
        color: white;
        font-size: 18px;
        font-weight: 600;
        margin-top: 3px;
    }}
    .hero-spm {{
        color: #FFD700;
        font-size: 15px;
        font-weight: bold;
        margin-top: 10px;
        border-top: 2px solid rgba(255,215,0,0.5);
        padding-top: 8px;
        letter-spacing: 1.5px;
    }}
    /* GLASSMORPHISM KPI - FIX TULISAN KEBAWAH TENGELAM ON PHONE */
    .kpi-card {{
        background: linear-gradient(135deg, rgba(0,105,92,0.95) 0%, rgba(0,77,64,0.98) 100%);
        backdrop-filter: blur(12px);
        border: 2.5px solid #FFD700;
        border-radius: 18px;
        padding: 14px 14px 10px 14px;
        min-height: 125px;
        height: auto;
        box-shadow: 0 8px 22px rgba(0,0,0,0.28), 0 0 18px rgba(255,215,0,0.18);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: visible;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }}
    .kpi-card:hover {{
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 16px 32px rgba(0,0,0,0.38), 0 0 28px rgba(255,215,0,0.65);
        border-color: #FFEB3B;
    }}
    .kpi-icon {{font-size: 26px; margin-bottom: 2px; filter: drop-shadow(0 0 8px rgba(255,215,0,0.7)); line-height: 1;}}
    .kpi-label {{color: #FFEB3B; font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.6px; line-height: 1.2; margin-bottom: 4px; min-height: 26px;}}
    .kpi-value {{color: #FFD700; font-size: 30px; font-weight: 800; margin-top: 2px; margin-bottom: 0px; text-shadow: 0 2px 10px rgba(255,215,0,0.5); font-family: 'Poppins', sans-serif; line-height: 1.1; word-break: break-all;}}
    /* RESPONSIVE PHONE FIX - elak tenggelam */
    @media (max-width: 768px) {{
        .kpi-card {{
            min-height: 110px;
            padding: 12px 10px 8px 10px;
            height: auto;
            overflow: visible;
        }}
        .kpi-icon {{font-size: 22px; margin-bottom: 1px;}}
        .kpi-label {{font-size: 9.5px; min-height: 22px; margin-bottom: 2px;}}
        .kpi-value {{font-size: 26px; margin-top: 1px;}}
        .hero-title {{font-size: 18px!important;}}
        .hero-subtitle {{font-size: 14px!important;}}
        .hero-spm {{font-size: 11px!important;}}
    }}
    /* BUTTON GLOW GOLD */
    button[kind="secondary"] {{
        background: linear-gradient(135deg, #00897B 0%, #004D40 100%)!important;
        color: #FFEB3B!important;
        border: 2.5px solid #FFD700!important;
        border-radius: 12px!important;
        font-weight: bold!important;
        transition: all 0.3s ease!important;
    }}
    button[kind="secondary"]:hover {{
        color: white!important;
        border-color: #FFEB3B!important;
        box-shadow: 0 0 20px rgba(255,215,0,0.85), 0 6px 18px rgba(0,0,0,0.35)!important;
        transform: translateY(-2.5px)!important;
    }}
    button[kind="primary"] {{
        background: linear-gradient(135deg, #C62828 0%, #B71C1C 100%)!important;
        border: 2.5px solid #FFD700!important;
        border-radius: 12px!important;
        font-weight: bold!important;
    }}
    button[kind="primary"]:hover {{
        box-shadow: 0 0 20px rgba(255,215,0,0.75)!important;
        transform: translateY(-2px)!important;
    }}
    .daerah-map-card {{
        background: linear-gradient(135deg, #E0F2F1 0%, #B2DFDB 100%);
        border: 2px solid #00897B;
        border-radius: 12px;
        padding: 10px 6px;
        text-align: center;
        transition: all 0.3s ease;
        height: 88px;
        cursor: pointer;
    }}
    .daerah-map-card:hover {{
        transform: scale(1.06);
        border-color: #FFD700;
        box-shadow: 0 0 18px rgba(255,215,0,0.6);
        background: linear-gradient(135deg, #004D40 0%, #00695C 100%);
    }}
    div[data-testid="stHorizontalBlock"] {{ align-items: flex-start!important; }}
    /* KOTAK METRIC HIJAU BALIK V31 - 504 & 10 DAERAH */
    div[data-testid="stMetric"] {{
        background: linear-gradient(135deg, #00897B 0%, #004D40 100%)!important;
        border: 2.5px solid #FFD700!important;
        border-radius: 15px!important;
        padding: 18px!important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25), 0 0 10px rgba(255,215,0,0.2)!important;
    }}
    div[data-testid="stMetric"] label {{
        color: #FFEB3B!important;
        font-weight: bold!important;
        font-size: 13px!important;
    }}
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {{
        color: #FFEB3B!important;
        font-weight: 800!important;
        font-size: 30px!important;
        text-shadow: 0 2px 6px rgba(0,0,0,0.3)!important;
    }}
    div[data-testid="stMetric"]:hover {{
        box-shadow: 0 6px 18px rgba(0,0,0,0.35), 0 0 18px rgba(255,215,0,0.5)!important;
        transform: translateY(-2px)!important;
    }}
    /* FILTER & MENU HIGH CONTRAST - FIX TENGELAM GELAP */
    div[data-testid="stSelectbox"] label p {{ 
        color: {filter_text}!important; 
        font-weight: 800!important; 
        font-size: 16px!important;
        text-shadow: 0 1px 3px rgba(0,0,0,0.5)!important;
    }}
    div[data-baseweb="select"] > div {{ 
        background-color: {filter_bg}!important; 
        border: 2.5px solid {filter_border}!important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3), 0 0 10px rgba(255,215,0,0.2)!important;
    }}
    div[data-baseweb="select"] span {{ 
        color: {filter_text}!important; 
        font-weight: bold!important;
        font-size: 15px!important;
    }}
    div[data-baseweb="select"] div {{ color: {filter_text}!important; }}
    /* SIDEBAR MENU BUTTONS - HIGH CONTRAST DARK MODE */
    section[data-testid="stSidebar"] button[kind="secondary"] {{
        background: linear-gradient(135deg, #00695C 0%, #004D40 100%)!important;
        color: #FFEB3B!important;
        border: 2.5px solid #FFD700!important;
        box-shadow: 0 3px 10px rgba(0,0,0,0.4), 0 0 12px rgba(255,215,0,0.25)!important;
    }}
    section[data-testid="stSidebar"] button[kind="secondary"]:hover {{
        background: linear-gradient(135deg, #00897B 0%, #00695C 100%)!important;
        color: white!important;
        border-color: #FFEB3B!important;
        box-shadow: 0 0 20px rgba(255,215,0,0.8)!important;
    }}
    /* MAIN CONTENT - PASTIKAN TEXT NAMPAK DALAM DARK MODE */
    div[data-testid="stAppViewContainer"] {{
        background: {dark_bg}!important;
    }}
    /* ANALISIS PANTAS BOX - DARK MODE FIX */
    div[data-testid="stMain"] {{
        color: #E0E0E0!important;
    }}

    /* EXTRA FIX - FILTER LABEL & PLACEHOLDER VISIBILITY */
    .stSelectbox label {{
        color: #FFEB3B!important;
    }}
    [data-baseweb="select"] input {{
        color: #FFEB3B!important;
    }}

    </style>
    """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- SISTEM NOTIS MARQUEE ---
FILE_NOTIS = "pemberitahuan.json"
DEFAULT_NOTIS = "📢 MAKLUMAN TERKINI:TAKLIMAT KESELAMATAN DAN PENGURUSAN SPM AKAN BERMULA PADA 21 HINGGA 30 SEPTEMBER MELIBATKAN 5 ZON. SEBARANG PERTANYAAN  SILA HUBUNGI SEKTOR PENTAKSIRAN DAN PEPERIKSAAN JPN SELANGOR"
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

# --- SESSION STATE - OTAK SISTEM (ingat data bila reload) ---
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
COLUMNS_MP_LENGKAP = ["Kod_PPD","No_Pusat","Nama_Pusat","KodMP","NamaMP","Kertas","Bil_Calon","Bil_Naskah","Kod_Bilik_Kebal","Nama_Bilik_Kebal","Kawasan","Pakej","NamaMP_Sebenar"]
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
def cari_file_excel():
    # Cari file excel walau nama besar-kecil lain (case-insensitive)
    kemungkinan = [
        "data_v1.1.xlsx", "Data-V1-1.xlsx", "Data_V1_1.xlsx", 
        "data_v1.1.XLSX", "data_v1.xlsx", "data.xlsx",
        "DATA_V1.1.xlsx", "Data-v1-1.xlsx"
    ]
    for nama in kemungkinan:
        if os.path.exists(nama):
            return nama
    # Cari apa saja file xlsx dalam folder yang ada perkataan data
    for f in os.listdir("."):
        if f.lower().endswith(".xlsx") and "data" in f.lower():
            return f
    return FILE_EXCEL

def load_data_pusat():
    file_excel = cari_file_excel()
    if os.path.exists(file_excel):
        try: 
            df = pd.read_excel(file_excel, sheet_name=SHEET_PUSAT, engine='openpyxl', dtype=str)
            # Jika kosong, cuba sheet lain
            if df.empty:
                # cuba baca tanpa nama sheet spesifik
                try:
                    xls = pd.ExcelFile(file_excel)
                    for sh in xls.sheet_names:
                        df_try = pd.read_excel(file_excel, sheet_name=sh, engine='openpyxl', dtype=str)
                        if not df_try.empty and 'No_Pusat' in df_try.columns:
                            return df_try
                except:
                    pass
            return df
        except Exception as e:
            st.warning(f"Ralat baca {file_excel}: {e}")
            return pd.DataFrame(columns=COLUMNS_PUSAT)
    else: 
        st.error(f"File {FILE_EXCEL} tak jumpa! Sila upload data_v1.1.xlsx di GitHub. File yang ada: {os.listdir('.')}")
        return pd.DataFrame(columns=COLUMNS_PUSAT)
def load_data_mp():
    file_excel = cari_file_excel()
    if os.path.exists(file_excel):
        try: 
            df = pd.read_excel(file_excel, sheet_name=SHEET_MP, engine='openpyxl', dtype=str)
            return df
        except: 
            # Jika sheet tak wujud atau kosong, return kosong tapi jangan error
            return pd.DataFrame(columns=COLUMNS_MP)
    else: 
        return pd.DataFrame(columns=COLUMNS_MP)
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

def parse_lp_format(uploaded_file):
    """Parse maklumat_pusat.xls format LP (Lembaga Peperiksaan) dengan 504 pusat"""
    try:
        import pandas as pd
        df_raw = pd.read_excel(uploaded_file, header=None)
        
        prefix_to_daerah = {
            "BA": "Klang", "BB": "Kuala Langat", "BC": "Kuala Selangor", "BD": "Hulu Langat",
            "BE": "Hulu Selangor", "BF": "Sabak Bernam", "BG": "Gombak", "BH": "Petaling Perdana",
            "BJ": "Sepang", "BK": "Petaling Utama",
        }
        daerah_to_kod = {
            "Klang": "ba", "Kuala Langat": "bb", "Kuala Selangor": "bc", "Hulu Langat": "bd",
            "Hulu Selangor": "be", "Sabak Bernam": "bf", "Gombak": "bg", "Petaling Perdana": "bh",
            "Sepang": "bj", "Petaling Utama": "bk",
        }
        
        records = []
        for idx, row in df_raw.iterrows():
            try:
                bil = row[0]
                if pd.notna(bil) and str(bil).strip().isdigit():
                    nombor_pusat = str(row[7]).strip() if pd.notna(row[7]) else ""
                    if not nombor_pusat or nombor_pusat == "NOMBOR" or len(nombor_pusat)<3:
                        continue
                    prefix = nombor_pusat[:2].upper()
                    nama_sekolah = str(row[11]).strip() if len(row)>11 and pd.notna(row[11]) else nombor_pusat
                    jumlah_calon = row[15] if len(row)>15 and pd.notna(row[15]) else 0
                    jumlah_di_pusat = row[22] if len(row)>22 and pd.notna(row[22]) else None
                    daerah = prefix_to_daerah.get(prefix, "Unknown")
                    
                    records.append({
                        "DAERAH": daerah,
                        "PREFIX": prefix,
                        "NOMBOR_PUSAT": nombor_pusat,
                        "NAMA_SEKOLAH": nama_sekolah,
                        "JUMLAH_CALON": jumlah_calon,
                        "JUMLAH_DI_PUSAT": jumlah_di_pusat,
                    })
            except:
                pass
        
        if not records:
            return False, "Tiada rekod ditemui dalam file LP. Pastikan format maklumat_pusat.xls"
        
        df = pd.DataFrame(records)
        pusat_group = df.groupby('NOMBOR_PUSAT').agg({
            'DAERAH': 'first',
            'NAMA_SEKOLAH': 'first',
            'JUMLAH_DI_PUSAT': 'first',
            'PREFIX': 'first',
            'JUMLAH_CALON': 'sum'
        }).reset_index()
        
        template_rows = []
        for _, r in pusat_group.iterrows():
            kod_ppd = daerah_to_kod.get(r['DAERAH'], r['PREFIX'].lower())
            bil = r['JUMLAH_DI_PUSAT']
            if pd.isna(bil) or bil == 0:
                bil = r['JUMLAH_CALON']
            try:
                bil_int = int(float(bil))
            except:
                bil_int = 0
            template_rows.append({
                "Kod_PPD": kod_ppd,
                "No_Pusat": r['NOMBOR_PUSAT'],
                "Nama_Pusat": str(r['NAMA_SEKOLAH'])[:100],
                "Bil_Calon_Pusat": bil_int,
                "Nama_Bilik_Kebal": "",
                "Dikemaskini_Oleh": "LP-Import",
                "Tarikh_Kemaskini": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
        
        df_pusat_new = pd.DataFrame(template_rows)
        
        # Merge dengan data sedia ada
        df_lama = st.session_state["data_pusat"]
        df_gabung = pd.concat([df_lama, df_pusat_new]).drop_duplicates(subset=['No_Pusat'], keep='last')
        st.session_state["data_pusat"] = df_gabung
        simpan_ke_excel()
        
        return True, f"Berjaya import {len(df_pusat_new)} pusat dari file LP (dari {len(records)} rekod sekolah). Jumlah calon: {df_pusat_new['Bil_Calon_Pusat'].sum():,}. Sekarang total pusat: {len(df_gabung)}"
    except Exception as e:
        return False, f"Ralat parse LP: {e}"



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
    # Form login putih bersih untuk popup sebelah button
    st.markdown("""
    <style>
    .login-popup {
        background: white;
        padding: 20px;
        border-radius: 15px;
        border: 3px solid #0D7377;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }

    /* EXTRA FIX - FILTER LABEL & PLACEHOLDER VISIBILITY */
    .stSelectbox label {{
        color: #FFEB3B!important;
    }}
    [data-baseweb="select"] input {{
        color: #FFEB3B!important;
    }}

    </style>
    """, unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("### 🔒 Log Masuk")
        username = st.text_input("Nama Pengguna", key="user_login_side", placeholder="Masukkan nama pengguna")
        password = st.text_input("Kata Laluan", type="password", key="pass_login_side", placeholder="Masukkan kata laluan")
        c1, c2 = st.columns(2)
        with c1:
            login_btn = st.button("Log Masuk", use_container_width=True, type="primary", key="btn_login_side")
        with c2:
            cancel_btn = st.button("Batal", use_container_width=True, key="btn_cancel_side")
        if login_btn:
            uname = username.lower().strip()
            if uname in USERS and USERS[uname]["password"] == password:
                st.session_state["editor_login"] = True
                st.session_state["username"] = uname
                st.session_state["role"] = USERS[uname]["role"]
                if USERS[uname]["role"] == "PPD":
                    st.session_state["daerah_ppd"] = USERS[uname]["daerah"]
                    st.session_state["kod_ppd"] = KOD_PPD[USERS[uname]["daerah"]]
                st.success(f"Berjaya login {uname}!")
                st.rerun()
            else:
                st.error("Salah!")


def page_cari_tarikh():
    st.header("📅 Cari Subjek Ikut Tarikh Peperiksaan")
    st.info("Masukkan tarikh untuk lihat subjek apa yang ada pada tarikh tersebut (ikut Jadual Rasmi SPM 2026) - 100 kertas")
    
    file_excel = cari_file_excel()
    df_jadual = pd.DataFrame()
    try:
        df_jadual = pd.read_excel(file_excel, sheet_name="Jadual_Rasmi_SPM2026", engine='openpyxl', dtype=str)
    except:
        try:
            df_jadual = pd.read_excel(file_excel, sheet_name="JADUAL PEPERIKSAAN", engine='openpyxl', dtype=str)
        except Exception as e:
            st.error(f"Jadual Rasmi tak jumpa dalam {file_excel}: {e}")
            return
    
    if df_jadual.empty:
        st.warning("Jadual kosong")
        return

    df_jadual['TARIKH'] = df_jadual['TARIKH'].astype(str)
    tarikh_list = sorted(df_jadual['TARIKH'].dropna().unique().tolist())
    
    col1,col2 = st.columns([2,1])
    with col1:
        selected_tarikh = st.selectbox("📅 Pilih Tarikh Peperiksaan (dari Jadual Rasmi SPM 2026)", tarikh_list, index=0, key="tarikh_select")
    with col2:
        cari_tarikh_text = st.text_input("Atau taip tarikh (contoh: 2026-12-16)", placeholder="2026-12-16", key="tarikh_text")
    
    if st.button("🔍 Cari Subjek Pada Tarikh", use_container_width=True, type="primary", key="btn_tarikh"):
        if cari_tarikh_text:
            df_filter = df_jadual[df_jadual['TARIKH'].astype(str).str.contains(cari_tarikh_text, case=False, na=False)]
            tarikh_display = cari_tarikh_text
        else:
            df_filter = df_jadual[df_jadual['TARIKH'] == selected_tarikh]
            tarikh_display = selected_tarikh
        
        if df_filter.empty:
            st.warning(f"Tiada subjek pada tarikh {tarikh_display}")
        else:
            st.success(f"✅ Jumpa {len(df_filter)} kertas peperiksaan pada tarikh {tarikh_display}")
            cols_show = [c for c in ['HARI','TARIKH','MASA MENJAWAB','KOD MATA PELAJARAN','KOD KERTAS','MATA PELAJARAN'] if c in df_filter.columns]
            st.dataframe(df_filter[cols_show], use_container_width=True)
            
            st.subheader(f"📚 Ringkasan Subjek pada {tarikh_display}")
            for _, row in df_filter.iterrows():
                kod = row.get('KOD KERTAS','') or row.get('KOD MATA PELAJARAN','')
                subjek = row.get('MATA PELAJARAN','')
                masa = row.get('MASA MENJAWAB','')
                hari = row.get('HARI','')
                st.markdown(f"- **{kod}** - {subjek} | ⏰ {masa} | 📅 {hari}")
    
    with st.expander("📋 Lihat Jadual Penuh SPM 2026 (100 kertas)"):
        st.dataframe(df_jadual, use_container_width=True, height=500)



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
                st.markdown("### 🟢 Upload Format LP (maklumat_pusat.xls) - Auto Convert 504 Pusat")
                st.caption("Upload file maklumat_pusat.xls dari Lembaga Peperiksaan - sistem akan auto parse semua daerah & jumlah calon")
                up_lp = st.file_uploader("Upload maklumat_pusat.xls (LP Format)", type=["xls","xlsx"], key="up_lp")
                if up_lp:
                    if st.button("🚀 Parse & Import File LP Sekarang", type="primary", use_container_width=True, key="btn_parse_lp"):
                        with st.spinner("Parsing file LP..."):
                            ok, msg = parse_lp_format(up_lp)
                            if ok:
                                st.success(msg)
                                st.balloons()
                                st.dataframe(st.session_state["data_pusat"].head(10), use_container_width=True)
                            else:
                                st.error(msg)
                st.write("---")
                st.markdown("### 🔵 Upload Template Biasa")


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
    if df_mp.empty: 
        st.warning("Sheet 'MataPelajaran' masih kosong.")
    else:
        col1, col2, col3, col4 = st.columns([2,2,1,2])
        with col1: cari_kod = st.text_input("1. Masukkan Kod Mata Pelajaran", placeholder="Contoh: 1103")
        with col2: cari_nama = st.text_input("2. ATAU Nama Mata Pelajaran", placeholder="Contoh: MATEMATIK")
        with col3: cari_kertas = st.selectbox("3. Pilih Kertas", ["Semua", "1", "2", "3", "4"])
        with col4: cari_daerah = st.selectbox("4. Pilih Daerah", ["Semua Daerah"] + list(KOD_PPD.keys()))
        
        if st.button("🔍 Cari Sekarang", type="primary", use_container_width=True):
            df_filter = df_mp.copy()
            if st.session_state.get("role") == "PPD": 
                df_filter = df_filter[df_filter["Kod_PPD"] == st.session_state["kod_ppd"]]
            else:
                if cari_daerah!= "Semua Daerah":
                    kod_ppd_pilihan = KOD_PPD[cari_daerah]
                    df_filter = df_filter[df_filter["Kod_PPD"] == kod_ppd_pilihan]
            
            # Filter kod / nama
            if cari_kod: 
                df_filter = df_filter[df_filter["KodMP"].str.contains(cari_kod, case=False, na=False)]
            elif cari_nama: 
                df_filter = df_filter[df_filter["NamaMP"].str.contains(cari_nama, case=False, na=False)]
            
            # FIX BERCAMPUR: Filter kertas dengan 2 syarat - Kertas column DAN NamaMP
            if cari_kertas != "Semua":
                # Cari yang Kertas column == pilihan DAN NamaMP mengandungi "Kertas X" (exact)
                import re
                pattern_kertas = rf"Kertas\s*{cari_kertas}\b"
                mask_kertas_col = df_filter["Kertas"].astype(str).str.strip() == str(cari_kertas)
                mask_nama = df_filter["NamaMP"].str.contains(pattern_kertas, case=False, na=False, regex=True)
                # Jika user pilih Kertas 1, kita nak yang betul2 Kertas 1 sahaja
                # Kalau data Excel bercampur, kita utamakan NamaMP yang ada Kertas X
                df_filter = df_filter[mask_kertas_col & mask_nama] if (mask_kertas_col & mask_nama).any() else df_filter[mask_kertas_col | mask_nama]
                
                # Detect data bercampur
                bercampur = df_filter[df_filter["Kertas"].astype(str).str.strip() != df_filter["NamaMP"].str.extract(rf"Kertas\s*(\d)", expand=False).fillna(df_filter["Kertas"].astype(str))]
                if not bercampur.empty:
                    st.warning(f"⚠️ Dikesan {len(bercampur)} rekod data bercampur! KodMP {cari_kod} - Kertas column tak sama dengan NamaMP. Sila betulkan di Excel.")
            
            if not df_filter.empty:
                jumlah_rekod = len(df_filter)
                jumlah_pusat_unik = df_filter.drop_duplicates(subset=["Kod_PPD", "No_Pusat"]).shape[0]
                st.success(f"✅ Jumpa {jumlah_rekod} rekod | {jumlah_pusat_unik} pusat")
                m1, m2 = st.columns(2)
                with m1: st.metric("Jumlah Rekod MP", f"{jumlah_rekod:,}")
                with m2: st.metric(f"Jumlah Pusat Tawar {cari_kod if cari_kod else cari_nama if cari_nama else 'MP'} Kertas {cari_kertas if cari_kertas!='Semua' else ''}", f"{jumlah_pusat_unik:,} pusat")
                
                # Show data
                cols_safe = [c for c in COLUMNS_MP_LENGKAP if c in df_filter.columns]
                if not cols_safe:
                    cols_safe = [c for c in COLUMNS_MP if c in df_filter.columns]
                if not cols_safe:
                    cols_safe = list(df_filter.columns)
                st.dataframe(df_filter[cols_safe].drop_duplicates(), use_container_width=True)
                
                # Button auto-betulkan
                if st.button("🛠️ Auto-Betulkan Kertas dari NamaMP (Jika Bercampur)"):
                    df_mp_full = st.session_state["data_mp"].copy()
                    # Extract Kertas dari NamaMP
                    df_mp_full["Kertas_Betul"] = df_mp_full["NamaMP"].str.extract(r"Kertas\s*(\d)", expand=False)
                    mask_fix = df_mp_full["Kertas_Betul"].notna() & (df_mp_full["Kertas"].astype(str).str.strip() != df_mp_full["Kertas_Betul"].str.strip())
                    if mask_fix.any():
                        df_mp_full.loc[mask_fix, "Kertas"] = df_mp_full.loc[mask_fix, "Kertas_Betul"]
                        df_mp_full.drop(columns=["Kertas_Betul"], inplace=True)
                        st.session_state["data_mp"] = df_mp_full
                        simpan_ke_excel()
                        st.success(f"✅ Berjaya betulkan {mask_fix.sum()} rekod! Kertas column kini ikut NamaMP.")
                        st.rerun()
                    else:
                        st.info("✅ Tiada data bercampur dikesan, semua Kertas column dah betul.")
            else: 
                st.error("⚠️ Tiada pusat yang menawarkan mata pelajaran tersebut - Cuba pilih 'Semua' untuk Kertas atau semak KodMP")

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

# HERO BANNER V47 SPM 2026 + COUNTDOWN LIVE WAKTU MALAYSIA FIX
from datetime import date, datetime
try:
    from zoneinfo import ZoneInfo
    MALAYSIA_TZ = ZoneInfo("Asia/Kuala_Lumpur")
except:
    MALAYSIA_TZ = None

# FIX: Guna waktu Malaysia, bukan UTC! Server Streamlit UTC, Malaysia UTC+8
try:
    if MALAYSIA_TZ:
        now_my = datetime.now(MALAYSIA_TZ)
    else:
        # fallback pytz
        import pytz
        now_my = datetime.now(pytz.timezone("Asia/Kuala_Lumpur"))
    HARI_INI_DISPLAY = now_my.date()
    JAM_MALAYSIA = now_my.strftime("%I:%M %p")
except:
    # Last fallback kalau zoneinfo/pytz takde
    from datetime import timedelta
    now_utc = datetime.utcnow()
    now_my = now_utc + timedelta(hours=8)  # Malaysia UTC+8 manual
    HARI_INI_DISPLAY = now_my.date()
    JAM_MALAYSIA = now_my.strftime("%I:%M %p")

from datetime import date as date_only
TARIKH_SPM = date_only(2026, 11, 23)
HARI_INI = HARI_INI_DISPLAY

delta = (TARIKH_SPM - HARI_INI_DISPLAY).days

# Auto-refresh countdown setiap 1 minit supaya tengah malam Malaysia auto tukar tarikh!
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=60000, key="countdown_live_my_refresh")  # refresh setiap 1 minit = 60000 ms - pastikan 12 malam terus update
except:
    pass
if delta < 0:
    countdown_text = "SPM SEDANG BERLANGSUNG!"
    countdown_num = "0"
    countdown_unit = "HARI LAGI"
else:
    countdown_text = f"{delta} HARI LAGI"
    countdown_num = str(delta)
    countdown_unit = "HARI LAGI MENUJU SPM BERTULIS"

# Warna ikut urgency
if delta <= 7:
    bg_countdown = "linear-gradient(135deg, #B71C1C 0%, #D32F2F 100%)"
    glow = "0 0 20px rgba(255,0,0,0.8)"
elif delta <= 30:
    bg_countdown = "linear-gradient(135deg, #E65100 0%, #FF6F00 100%)"
    glow = "0 0 18px rgba(255,111,0,0.7)"
else:
    bg_countdown = "linear-gradient(135deg, #004D40 0%, #00695C 100%)"
    glow = "0 0 15px rgba(255,215,0,0.6)"

if os.path.exists("logo.png"):
    with open("logo.png", "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode()
        logo_html = f'<img src="data:image/png;base64,{logo_b64}" width="115" style="border:3px solid #FFD700; border-radius:14px; box-shadow: 0 0 15px rgba(255,215,0,0.6);">'
else: 
    logo_html = '<div style="font-size:55px; filter: drop-shadow(0 0 10px gold);">🏛️</div>'

st.markdown(f"""
<div class="hero-banner">
    <div style="display: flex; align-items: center; position: relative; z-index: 1;">
        <div style="margin-right: 22px;">{logo_html}</div>
        <div>
            <div class="hero-title">JABATAN PENDIDIKAN SELANGOR</div>
            <div class="hero-subtitle">SEKTOR PENTAKSIRAN DAN PEPERIKSAAN</div>
            <div class="hero-spm">✨ SIJIL PELAJARAN MALAYSIA 2026 ✨ | SISTEM PENGURUSAN PEPERIKSAAN SPM SELANGOR</div>
            <div style="margin-top:6px; font-size:11px; color:#FFEB3B; opacity:0.9;">📅 SPM Bertulis: 23 November 2026 | Hari ini: {HARI_INI_DISPLAY.strftime('%d %B %Y')} | 🕐 {JAM_MALAYSIA} MY</div>
        </div>
        <div style="margin-left: auto; text-align: right;">
            <div class="countdown-box" style="background: {bg_countdown}; border: 3px solid #FFD700; border-radius: 14px; padding: 10px 16px; box-shadow: {glow}; min-width: 135px; text-align:center; animation: blinkGold 1.2s infinite;">
                <div class="countdown-label" style="color: #FFEB3B; font-size: 11px; font-weight: 900; letter-spacing:1px; animation: textBlink 0.8s infinite;">⏳ COUNTDOWN SPM</div>
                <div class="countdown-number" style="color: white; font-size: 38px; font-weight: 900; line-height:1; margin:5px 0; text-shadow: 0 2px 8px rgba(0,0,0,0.5); animation: numberPulse 1s infinite;">{countdown_num}</div>
                <div style="color: #FFD700; font-size: 11px; font-weight: 800; animation: textBlink 1s infinite;">{countdown_unit}</div>
                <div style="color: white; font-size: 10px; margin-top:3px; opacity:0.9; font-weight:bold;">📅 23 NOV 2026</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

col_sidebar, col_main = st.columns([1, 4])
with col_sidebar:
    # DARK MODE TOGGLE V28
    col_dark1, col_dark2 = st.columns([3,1])
    with col_dark1:
        st.markdown("### Menu")
    with col_dark2:
        if st.button("🌙" if not st.session_state["dark_mode"] else "☀️", key="toggle_dark"):
            st.session_state["dark_mode"] = not st.session_state["dark_mode"]
            st.rerun()
    
    if st.session_state["dark_mode"]:
        st.caption("🌙 Dark Mode SPM 2026")
    else:
        st.caption("☀️ Light Mode SPM 2026")
    if st.button("📊 Dashboard", use_container_width=True): st.session_state["menu"] = "Dashboard"; st.rerun()
    if st.button("📅 Jadual Waktu", use_container_width=True): st.session_state["menu"] = "Jadual"; st.rerun()
    if st.button("📋 Senarai Pusat", use_container_width=True): st.session_state["menu"] = "SenaraiPusat"; st.rerun()
    if st.button("📚 Cari Mata Pelajaran", use_container_width=True): st.session_state["menu"] = "CariMP"; st.rerun()
    if st.button("📅 Cari Ikut Tarikh", use_container_width=True): st.session_state["menu"] = "CariTarikh"; st.rerun()
    
    # SELENGGARA DATA - KEDUDUKAN LAMA DI SIDEBAR (BETUL) - POPUP SEBELAH
    if not st.session_state.get("editor_login", False):
        with st.popover("🛠️ Selenggara Data", use_container_width=True):
            login_editor()
    else:
        if st.button("🛠️ Selenggara Data", use_container_width=True, type="primary"):
            st.session_state["menu"] = "Selenggara"; st.rerun()
        st.success(f"✅ {st.session_state['username']}")
        if st.button("Log Keluar", use_container_width=True):
            st.session_state["editor_login"] = False
            st.session_state["menu"] = "Dashboard"
            st.rerun()
        if st.button("🛠️ Selenggara Pusat", use_container_width=True, type="primary"): 
            st.session_state["menu"] = "Selenggara"; st.rerun()
    
    st.write("---")
    st.markdown("### 🔗 Pautan Sistem Lain")
    st.markdown("""<a href="https://sppat.moe.gov.my" target="_blank" style="display:block; text-align:center; background:linear-gradient(135deg, #00897B 0%, #004D40 100%); border:2px solid #FFD700; color:#FFEB3B; padding:10px; border-radius:10px; text-decoration:none; font-weight:bold; margin-bottom:10px;">1. SPPAT</a>""", unsafe_allow_html=True)
    st.markdown("""<a href="https://elp.moe.gov.my/eportal/login" target="_blank" style="display:block; text-align:center; background:linear-gradient(135deg, #00897B 0%, #004D40 100%); border:2px solid #FFD700; color:#FFEB3B; padding:10px; border-radius:10px; text-decoration:none; font-weight:bold; margin-bottom:10px;">2. ELP Portal</a>""", unsafe_allow_html=True)
    st.markdown("""<a href="https://sistem-amali-sains-selangor-2026.streamlit.app/" target="_blank" style="display:block; text-align:center; background:linear-gradient(135deg, #00897B 0%, #004D40 100%); border:2px solid #FFD700; color:#FFEB3B; padding:10px; border-radius:10px; text-decoration:none; font-weight:bold; margin-bottom:10px;">3. UAS - Amali Sains 2026</a>""", unsafe_allow_html=True)
    if st.session_state.get("editor_login", False):
        st.link_button("4. Selenggara Calon PPD", "https://script.google.com/macros/s/AKfycbwav3jbWQEkTW2yTK9PnanlItxPM5NpCHADLNb_BRjY4hmsale257tSqMsRTdqv88HA/exec", use_container_width=True, type="primary")
        st.write("---")
        st.markdown("### 📁 Pautan Pengurusan")
        st.link_button("5. Pengurusan", LINK_PENGURUSAN, use_container_width=True, type="primary")
        st.link_button("6. Sistem IPEP Selangor", "http://ipep.my/selangor/", use_container_width=True, type="primary")
    # END SIDEBAR
    st.write("---")
    # OLD BLOCK REMOVED - POPUP NOW
    if False:
        st.write("---")
        if not st.session_state.get("editor_login", False): login_editor()
        else:
            st.success(f"Login: **{st.session_state['username']}**")
            st.caption(f"Role: **{st.session_state['role']}**")
            if st.button("Log Keluar", use_container_width=True): st.session_state["editor_login"] = False; st.session_state["show_editor"] = False; st.session_state["menu"] = "Dashboard"; st.rerun()
    if st.session_state["menu"] == "Dashboard":
        # Filters akan di-handle di main area (atas), bukan sidebar lagi
        pass
    daerah, jenis_data, sub_filter = "Semua Daerah", "Semua", "Semua"

with col_main:
    if st.session_state["menu"] == "Dashboard":
        data = st.session_state["data_calon"]
        # ===== V14 - ANGKA ATAS, FILTER BAWAH - BY AIRA =====
        # Default values dulu, filter akan set di bawah nanti - tapi untuk kiraan kita guna session state
        if "filter_daerah_v14" not in st.session_state:
            st.session_state["filter_daerah_v14"] = "Semua Daerah"
        if "filter_jenis_v14" not in st.session_state:
            st.session_state["filter_jenis_v14"] = "Semua"
        if "filter_sub_v14" not in st.session_state:
            st.session_state["filter_sub_v14"] = "Semua"
        
        daerah = st.session_state["filter_daerah_v14"]
        jenis_data = st.session_state["filter_jenis_v14"]
        sub_filter = st.session_state["filter_sub_v14"]


        # ===== FIX DINAMIK OLEH AIRA - ikut filter =====
        # Calon
        if daerah == "Semua Daerah":
            if jenis_data == "Calon" and sub_filter != "Semua Jenis":
                jumlah_calon_total = sum(data[d].get(sub_filter, 0) for d in data)
                label_calon = f"Jumlah Calon {sub_filter}"
            else:
                jumlah_calon_total = sum(sum(data[d][k] for k in JENIS_CALON[1:]) for d in data)
                label_calon = "Jumlah Calon Keseluruhan"
            # Petugas
            if jenis_data == "Petugas" and sub_filter != "Semua Jawatan":
                jumlah_petugas_total = sum(data[d].get(sub_filter, 0) for d in data)
                label_petugas = f"Jumlah {sub_filter} Keseluruhan"
            else:
                jumlah_petugas_total = sum(sum(data[d][k] for k in JENIS_PETUGAS[1:]) for d in data)
                label_petugas = "Jumlah Petugas Keseluruhan"
            jumlah_pusat_total = sum(data[d]["Ketua Pengawas"] for d in data)
            label_pusat = "Jumlah Pusat Keseluruhan"
        else:
            if jenis_data == "Calon" and sub_filter != "Semua Jenis":
                jumlah_calon_total = data[daerah].get(sub_filter, 0)
                label_calon = f"Jumlah Calon {sub_filter} - {daerah}"
            else:
                jumlah_calon_total = sum(data[daerah][k] for k in JENIS_CALON[1:])
                label_calon = f"Jumlah Calon {daerah}"
            if jenis_data == "Petugas" and sub_filter != "Semua Jawatan":
                jumlah_petugas_total = data[daerah].get(sub_filter, 0)
                label_petugas = f"Jumlah {sub_filter} - {daerah}"
            else:
                jumlah_petugas_total = sum(data[daerah][k] for k in JENIS_PETUGAS[1:])
                label_petugas = f"Jumlah Petugas {daerah}"
            jumlah_pusat_total = data[daerah]["Ketua Pengawas"]
            label_pusat = f"Jumlah Pusat {daerah}"

        # Biru muda dibuang terus - tiada info box
        pass

        # GLASSMORPHISM ANIMATED KPI CARDS V28 SPM 2026
        colA, colB, colC = st.columns(3)
        with colA:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon">🎓</div>
                <div class="kpi-label">{label_calon}</div>
                <div class="kpi-value">{jumlah_calon_total:,}</div>
            </div>
            """, unsafe_allow_html=True)
        with colB:
            st.markdown(f"""
            <div class="kpi-card" style="background: linear-gradient(135deg, rgba(121,85,72,0.9) 0%, rgba(62,39,35,0.95) 100%); min-height: 125px;">
                <div class="kpi-icon">👮</div>
                <div class="kpi-label">{label_petugas}</div>
                <div class="kpi-value">{jumlah_petugas_total:,}</div>
            </div>
            """, unsafe_allow_html=True)
        with colC:
            st.markdown(f"""
            <div class="kpi-card" style="background: linear-gradient(135deg, rgba(2,119,189,0.9) 0%, rgba(1,87,155,0.95) 100%); min-height: 125px;">
                <div class="kpi-icon">🏫</div>
                <div class="kpi-label">{label_pusat}</div>
                <div class="kpi-value">{jumlah_pusat_total:,}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<style>@keyframes countUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }</style>", unsafe_allow_html=True)

# ===== V16 - FILTER CANTIK TANPA TIPS - ANGKA ATAS FILTER BAWAH =====
        st.write("")
        st.markdown('''
        <style>
        div[data-testid="stSelectbox"] > div > div {
            background: white !important;
            border: 2px solid #0D7377 !important;
            border-radius: 12px !important;
            box-shadow: 0 2px 8px rgba(13,115,119,0.15) !important;
        }
        div[data-testid="stSelectbox"] label {
            font-weight: 700 !important;
            color: #0D7377 !important;
        }
        </style>
        ''', unsafe_allow_html=True)
        f1, f2, f3 = st.columns([1.2, 1, 1.2], gap="medium")
        with f1:
            daerah_list = ["Semua Daerah"] + list(data.keys())
            daerah_new = st.selectbox("📍 Pilih Daerah:", daerah_list, key="filter_daerah_v14_select", index=daerah_list.index(daerah) if daerah in daerah_list else 0)
        with f2:
            jenis_list = ["Calon", "Petugas", "Semua"]
            jenis_new = st.selectbox("📊 Pilih Data:", jenis_list, key="filter_jenis_v14_select", index=jenis_list.index(jenis_data) if jenis_data in jenis_list else 2)
        with f3:
            if jenis_new == "Calon":
                sub_new = st.selectbox("🎓 Pilih Jenis Calon:", JENIS_CALON, key="filter_sub1_v14_select")
            elif jenis_new == "Petugas":
                sub_new = st.selectbox("👮 Pilih Jawatan Petugas:", JENIS_PETUGAS, key="filter_sub2_v14_select")
            else:
                sub_new = "Semua"
                st.selectbox("📋 Paparan:", ["Semua Data"], disabled=True, key="filter_all_v14_select")

        # Update session if changed and rerun to update angka atas
        if daerah_new != daerah or jenis_new != jenis_data or sub_new != sub_filter:
            st.session_state["filter_daerah_v14"] = daerah_new
            st.session_state["filter_jenis_v14"] = jenis_new
            st.session_state["filter_sub_v14"] = sub_new
            st.rerun()

        st.write("---")
        # ===== V26 POWER DASHBOARD - AUTO WARNING + PIE + RATIO =====
        total_calon_check = sum(sum(data[d][k] for k in JENIS_CALON[1:]) for d in data)
        total_pusat_check = sum(data[d]["Ketua Pengawas"] for d in data)
        if total_calon_check > 0 and total_pusat_check > 0:
            ratio = total_calon_check / total_pusat_check if total_pusat_check > 0 else 0
            st.markdown(f'''
            <div style="background: linear-gradient(135deg, #E0F2F1 0%, #B2DFDB 100%); border: 2px solid #00897B; border-radius: 12px; padding: 12px 18px; margin-bottom: 15px;">
                <b style="color: #004D40;">📈 Analisis Pantas:</b> 
                <span style="color: #00695C;">Nisbah Calon : Pusat = <b>{ratio:.1f} calon/pusat</b> | Jumlah Calon: <b>{total_calon_check:,}</b> | Pusat: <b>{total_pusat_check:,}</b></span>
            </div>
            ''', unsafe_allow_html=True)

        if jenis_data == "Calon" or jenis_data == "Semua":
            st.subheader("📊 Bilangan Calon Mengikut Daerah")
            df_calon = pd.DataFrame([{k: v[k] for k in JENIS_CALON[1:]} for v in data.values()], index=data.keys())
            if daerah!= "Semua Daerah": df_calon = df_calon.loc[[daerah]]
            if sub_filter!= "Semua Jenis" and jenis_data == "Calon": df_calon = df_calon[[sub_filter]]
            st.dataframe(df_calon, use_container_width=True)
            if PLOTLY_AVAILABLE:
                df_calon_plot = df_calon.reset_index().melt(id_vars='index', var_name='Jenis Calon', value_name='Bilangan')
                df_calon_plot.rename(columns={'index':'Daerah'}, inplace=True)
                fig1 = px.bar(df_calon_plot, x='Daerah', y='Bilangan', color='Jenis Calon', 
                              barmode='group', height=550,
                              color_discrete_sequence=['#0D7377', '#FFD700', '#D32F2F', '#1976D2', '#388E3C', '#F57C00', '#7B1FA2', '#0097A7'])
                fig1.update_layout(xaxis_tickangle=-35, legend_title="Jenis Calon", 
                                   yaxis_title="Bilangan Calon", xaxis_title="Daerah",
                                   font=dict(color="black"), plot_bgcolor="white")
                fig1.update_traces(hovertemplate='<b>%{x}</b><br>%{fullData.name}: %{y:,}<extra></extra>', marker=dict(line=dict(width=1.5, color='white'), opacity=0.9))
                st.plotly_chart(fig1, use_container_width=True)
                
                st.markdown("#### 🥧 Pecahan Jenis Calon Keseluruhan")
                pie_data = df_calon.sum().reset_index()
                pie_data.columns = ['Jenis', 'Bilangan']
                fig_pie = px.pie(pie_data, values='Bilangan', names='Jenis', hole=0.4,
                                 color_discrete_sequence=['#0D7377', '#FFCA28', '#EF5350', '#42A5F5', '#66BB6A', '#FFA726', '#26C6DA', '#AB47BC'])
                fig_pie.update_traces(textinfo='percent+label', textfont_size=12)
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                fig1, ax1 = plt.subplots(figsize=(13, 6.5))
                df_calon.plot(kind='bar', ax=ax1, width=0.75, color=['#0D7377', '#FFD700', '#D32F2F', '#1976D2', '#388E3C', '#F57C00'])
                ax1.set_ylabel("Bilangan Calon", fontweight='bold', fontsize=12, color='black')
                ax1.set_xlabel("Daerah", fontweight='bold', fontsize=12, color='black')
                for label in ax1.get_xticklabels(): label.set_fontweight('bold'); label.set_rotation(35); label.set_ha('right')
                ax1.legend(title="Jenis Calon", bbox_to_anchor=(1.05, 1), loc='upper left')
                for container in ax1.containers:
                    labels = [f"{int(v)}" if v > 400 else "" for v in container.datavalues]
                    ax1.bar_label(container, labels=labels, label_type='edge', fontsize=9, fontweight='bold', padding=3)
                plt.tight_layout(); st.pyplot(fig1)

        if jenis_data == "Petugas" or jenis_data == "Semua":
            st.write("---")
            st.subheader("👮 Bilangan Petugas Mengikut Daerah")
            df_petugas = pd.DataFrame([{k: v[k] for k in JENIS_PETUGAS[1:]} for v in data.values()], index=data.keys())
            if daerah!= "Semua Daerah": df_petugas = df_petugas.loc[[daerah]]
            if sub_filter!= "Semua Jawatan" and jenis_data == "Petugas": df_petugas = df_petugas[[sub_filter]]
            st.dataframe(df_petugas, use_container_width=True)
            if PLOTLY_AVAILABLE:
                df_petugas_plot = df_petugas.reset_index().melt(id_vars='index', var_name='Jawatan', value_name='Bilangan')
                df_petugas_plot.rename(columns={'index':'Daerah'}, inplace=True)
                fig2 = px.bar(df_petugas_plot, x='Daerah', y='Bilangan', color='Jawatan',
                              barmode='group', height=600,
                              color_discrete_sequence=['#004D40', '#C62828', '#1565C0', '#AB47BC', '#2E7D32', '#EF6C00', '#FFD600'])
                fig2.update_layout(xaxis_tickangle=-35, legend_title="Jawatan Petugas",
                                   yaxis_title="Bilangan Petugas", xaxis_title="Daerah",
                                   font=dict(color="black"), plot_bgcolor="white")
                fig2.update_traces(hovertemplate='<b>%{x}</b><br>%{fullData.name}: %{y:,}<extra></extra>', marker=dict(line=dict(width=1.5, color='white'), opacity=0.9))
                st.plotly_chart(fig2, use_container_width=True)
                
                st.markdown("#### ⚖️ Nisbah Petugas vs Calon Mengikut Daerah")
                df_ratio = pd.DataFrame({
                    'Daerah': list(data.keys()),
                    'Calon': [sum(data[d][k] for k in JENIS_CALON[1:]) for d in data.keys()],
                    'Pengawas': [data[d].get('Pengawas', 0) for d in data.keys()]
                })
                fig_ratio = go.Figure()
                fig_ratio.add_trace(go.Bar(name='Calon', x=df_ratio['Daerah'], y=df_ratio['Calon'], marker=dict(color='#00ACC1', line=dict(width=1.5, color='white'))))
                fig_ratio.add_trace(go.Bar(name='Pengawas', x=df_ratio['Daerah'], y=df_ratio['Pengawas'], marker=dict(color='#FFA000', line=dict(width=1.5, color='white'))))
                fig_ratio.update_layout(barmode='group', height=500, xaxis_tickangle=-35,
                                        yaxis_title="Bilangan", xaxis_title="Daerah")
                st.plotly_chart(fig_ratio, use_container_width=True)
            else:
                fig2, ax2 = plt.subplots(figsize=(13, 6.5))
                df_petugas.plot(kind='bar', ax=ax2, width=0.75, color=['#004D40', '#C62828', '#1565C0', '#AB47BC', '#2E7D32', '#EF6C00'])
                ax2.set_ylabel("Bilangan Petugas", fontweight='bold', fontsize=12, color='black')
                ax2.set_xlabel("Daerah", fontweight='bold', fontsize=12, color='black')
                for label in ax2.get_xticklabels(): label.set_fontweight('bold'); label.set_rotation(35); label.set_ha('right')
                ax2.legend(title="Jawatan Petugas", bbox_to_anchor=(1.05, 1), loc='upper left')
                for container in ax2.containers:
                    jawatan = container.get_label()
                    if "Pengawas" in jawatan:
                        labels = [f"{int(v)}" if v > 150 else "" for v in container.datavalues]
                        ax2.bar_label(container, labels=labels, label_type='edge', fontsize=9, fontweight='bold', padding=3)
                plt.tight_layout(); st.pyplot(fig2)
    elif st.session_state["menu"] == "Jadual":
        st.subheader("📅 Jadual Waktu SPM 2026")
        st.info("💡 Sistem tidak akan auto-download. Sila pilih apa yang anda nak buat di bawah.")
        
        LINK_JADUAL_PDF = "https://raw.githubusercontent.com/akashahismail-create/sistem-jpn-selangor/main/Jadual_Waktu_SPM.pdf"
        
        col1, col2 = st.columns(2)
        with col1:
            lihat_jadual = st.checkbox("👁️ Ya, saya nak LIHAT Jadual Waktu", key="lihat_jadual_cb")
        with col2:
            nak_download = st.checkbox("📥 Ya, saya nak DOWNLOAD Jadual Waktu", key="download_jadual_cb")
        
        st.markdown("---")
        
        if lihat_jadual:
            st.success("✅ Papar Jadual Waktu SPM 2026 di bawah:")
            st.markdown(f'<iframe src="{LINK_JADUAL_PDF}" width="100%" height="800" type="application/pdf"></iframe>', unsafe_allow_html=True)
        else:
            st.caption("☝️ Tick 'LIHAT' di atas untuk papar Jadual Waktu")
        
        if nak_download:
            st.warning("⚠️ Anda pilih untuk download Jadual Waktu SPM 2026")
            st.markdown(f"📥 **Link Download:** [Klik sini untuk Muat Turun Jadual Waktu]({LINK_JADUAL_PDF})")
            # Confirmation buttons
            c_yes, c_no = st.columns(2)
            with c_yes:
                if st.button("✅ Ya, Download Sekarang", type="primary", use_container_width=True, key="btn_dl_yes"):
                    st.markdown(f'<a href="{LINK_JADUAL_PDF}" download target="_blank">📥 Download bermula...</a>', unsafe_allow_html=True)
                    st.success("📥 Download bermula! Check folder Downloads anda.")
            with c_no:
                if st.button("❌ Batal Download", use_container_width=True, key="btn_dl_no"):
                    st.session_state["download_jadual_cb"] = False
                    st.rerun()
        else:
            st.caption("☝️ Tick 'DOWNLOAD' di atas jika anda nak download Jadual Waktu")
    elif st.session_state["menu"] == "Selenggara": page_selenggara_pusat()
    elif st.session_state["menu"] == "CariMP":
        page_cari_mp()
    elif st.session_state["menu"] == "CariTarikh":
        page_cari_tarikh()
    elif st.session_state["menu"] == "SenaraiPusat": page_senarai_pusat()
    
    # FOOTER CANTIK SPM 2026
    st.markdown("---")
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #004D40 0%, #00695C 100%); border: 2px solid #FFD700; border-radius: 15px; padding: 14px 20px; text-align: center; margin-top: 25px;">
        <div style="color: #FFD700; font-weight: 800; font-size: 14px; letter-spacing: 1px;">© 2026 JABATAN PENDIDIKAN SELANGOR | SEKTOR PENTAKSIRAN DAN PEPERIKSAAN</div>
        <div style="color: white; font-size: 13px; margin-top: 5px; font-weight: 600;">Sistem Pengurusan Peperiksaan SPM 2026</div>
        <div style="color: #B2DFDB; font-size: 11px; margin-top: 6px;">✨ SPM 2026 - Cemerlang Bersama ✨</div>
    </div>
    """, unsafe_allow_html=True)
