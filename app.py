
import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Sistem JPN Selangor SPM 2026", layout="wide", page_icon="📚")

FILE_EXCEL = "data_v1.1.xlsx"
SHEET_PUSAT = "selenggara_pusat"
SHEET_MP = "MataPelajaran"
SHEET_JADUAL = "Jadual_Rasmi_SPM2026"

COLUMNS_PUSAT = ["Kod_PPD","No_Pusat","Nama_Pusat","Bil_Calon_Pusat","Kod_Bilik_Kebal","Nama_Bilik_Kebal","Dikemaskini_Oleh","Tarikh_Kemaskini"]
COLUMNS_MP_LENGKAP = ["Kod_PPD","No_Pusat","Nama_Pusat","KodMP","NamaMP","Kertas","Bil_Calon","Bil_Naskah","Bil_Calon_Batch","Kod_Bilik_Kebal","Nama_Bilik_Kebal","Kawasan","Pakej","Bil_Calon_Pusat","NamaMP_Sebenar"]

def cari_file_excel():
    for f in [FILE_EXCEL, "./data_v1.1.xlsx", "/mnt/data/data_v1.1.xlsx", "data_v1.1_FINAL_JADUAL_RASMI.xlsx"]:
        if os.path.exists(f):
            return f
    return FILE_EXCEL

def load_data_pusat():
    file_excel = cari_file_excel()
    if os.path.exists(file_excel):
        try: 
            df = pd.read_excel(file_excel, sheet_name=SHEET_PUSAT, engine='openpyxl', dtype=str)
            if 'Kod_PPD' in df.columns:
                df['Kod_PPD'] = df['Kod_PPD'].astype(str).str.upper()
            if 'Kod_Bilik_Kebal' in df.columns:
                df['Kod_Bilik_Kebal'] = df['Kod_Bilik_Kebal'].astype(str).str.upper()
            return df
        except Exception as e:
            st.error(f"Ralat baca pusat: {e}")
            return pd.DataFrame(columns=COLUMNS_PUSAT)
    else: 
        st.error(f"File {FILE_EXCEL} tak jumpa!")
        return pd.DataFrame(columns=COLUMNS_PUSAT)

def load_data_mp():
    file_excel = cari_file_excel()
    if os.path.exists(file_excel):
        try: 
            df = pd.read_excel(file_excel, sheet_name=SHEET_MP, engine='openpyxl', dtype=str)
            if 'Kod_PPD' in df.columns:
                df['Kod_PPD'] = df['Kod_PPD'].astype(str).str.upper()
            if 'Kod_Bilik_Kebal' in df.columns:
                df['Kod_Bilik_Kebal'] = df['Kod_Bilik_Kebal'].astype(str).str.upper()
            return df
        except Exception as e:
            st.error(f"Ralat baca MP: {e}")
            return pd.DataFrame()
    else:
        return pd.DataFrame()

def load_jadual():
    file_excel = cari_file_excel()
    try:
        df = pd.read_excel(file_excel, sheet_name=SHEET_JADUAL, engine='openpyxl', dtype=str)
        return df
    except:
        try:
            df = pd.read_excel(file_excel, sheet_name="JADUAL PEPERIKSAAN", engine='openpyxl', dtype=str)
            return df
        except Exception as e:
            return pd.DataFrame()

def to_excel(df):
    from io import BytesIO
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

# Session
if "data_pusat" not in st.session_state:
    st.session_state["data_pusat"] = load_data_pusat()
if "data_mp" not in st.session_state:
    st.session_state["data_mp"] = load_data_mp()

def page_dashboard():
    st.header("📊 Dashboard SPM 2026 Selangor")
    df_pusat = st.session_state["data_pusat"]
    df_mp = st.session_state["data_mp"]
    
    if not df_pusat.empty:
        total_pusat = len(df_pusat)
        total_calon = pd.to_numeric(df_pusat['Bil_Calon_Pusat'], errors='coerce').sum()
        m1,m2,m3 = st.columns(3)
        m1.metric("Jumlah Pusat", f"{total_pusat:,}")
        m2.metric("Jumlah Calon", f"{total_calon:,.0f}")
        m3.metric("Jumlah MP Unik", f"{df_mp['KodMP'].nunique() if not df_mp.empty else 0}")
        
        # By PPD
        if 'Kod_PPD' in df_pusat.columns:
            st.subheader("Ikut PPD")
            df_ppd = df_pusat.groupby('Kod_PPD').agg(Bil_Pusat=('No_Pusat','count'), Jumlah_Calon=('Bil_Calon_Pusat', lambda x: pd.to_numeric(x, errors='coerce').sum())).reset_index()
            st.dataframe(df_ppd, use_container_width=True)

def page_cari_mp():
    st.header("🔍 Carian Mata Pelajaran Mengikut Pusat")
    df_mp = st.session_state["data_mp"]
    
    if df_mp.empty:
        st.warning("Data MP kosong!")
        return

    col1,col2,col3 = st.columns(3)
    with col1:
        cari_kod = st.text_input("1. Kod Mata Pelajaran", placeholder="Contoh: 4531, 4541, 9217...", key="kod_mp")
    with col2:
        cari_nama = st.text_input("2. Nama Mata Pelajaran", placeholder="Contoh: FIZIK, KIMIA, Kesusasteraan Tamil...", key="nama_mp", help="Taip FIZIK, KIMIA, EKONOMI, Kesusasteraan Melayu, Turath Al-Quran dll")
    with col3:
        kertas_list = ["Semua"] + sorted(df_mp['Kertas'].dropna().unique().tolist())
        cari_kertas = st.selectbox("3. Kertas", kertas_list, key="kertas_mp")

    if st.button("🔍 Cari", use_container_width=True):
        df_filter = df_mp.copy()
        
        if cari_kod:
            df_filter = df_filter[df_filter['KodMP'].astype(str).str.contains(cari_kod, case=False, na=False)]
        if cari_nama:
            mask = df_filter['NamaMP'].astype(str).str.contains(cari_nama, case=False, na=False)
            if 'NamaMP_Sebenar' in df_filter.columns:
                mask = mask | df_filter['NamaMP_Sebenar'].astype(str).str.contains(cari_nama, case=False, na=False)
            df_filter = df_filter[mask]
        if cari_kertas != "Semua":
            df_filter = df_filter[df_filter['Kertas'].astype(str) == str(cari_kertas)]
        
        if df_filter.empty:
            st.warning("❌ Tiada pusat yang menawarkan mata pelajaran tersebut. Cuba pilih 'Semua' untuk Kertas atau semak Kod/Nama.")
            st.info("💡 Tips: Kod 4531=FIZIK, 4541=KIMIA, 9217=Kesusasteraan Tamil, 9216=Kesusasteraan Cina, 2216=Kesusasteraan Melayu, 2206=Kesusasteraan Inggeris, 5303=Turath Al-Quran")
        else:
            jumlah_rekod = len(df_filter)
            jumlah_pusat_unik = df_filter.drop_duplicates(subset=["No_Pusat"]).shape[0]
            st.success(f"✅ Jumpa {jumlah_rekod} rekod | {jumlah_pusat_unik} pusat")
            m1,m2,m3 = st.columns(3)
            with m1: st.metric("Jumlah Rekod MP", f"{jumlah_rekod:,}")
            with m2: st.metric(f"Pusat Tawar", f"{jumlah_pusat_unik:,} pusat")
            try:
                df_unique = df_filter.drop_duplicates(subset=["No_Pusat"])
                total_calon = pd.to_numeric(df_unique['Bil_Calon_Pusat'], errors='coerce').sum() if 'Bil_Calon_Pusat' in df_unique.columns else pd.to_numeric(df_unique['Bil_Calon'], errors='coerce').sum()
                with m3: st.metric("Jumlah Calon (Unique Pusat)", f"{total_calon:,.0f}")
            except:
                with m3: st.metric("Jumlah Calon", "-")
            
            cols_show = [c for c in ["Kod_PPD","No_Pusat","Nama_Pusat","KodMP","NamaMP","Kertas","Bil_Calon","Bil_Naskah","Kod_Bilik_Kebal","Nama_Bilik_Kebal","Kawasan","Pakej"] if c in df_filter.columns]
            st.dataframe(df_filter[cols_show].drop_duplicates(), use_container_width=True, height=500)
            
            st.download_button("📥 Download Hasil Carian (Excel)", to_excel(df_filter[cols_show]), f"carian_{cari_kod or cari_nama or 'MP'}_kertas{cari_kertas}.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

def page_cari_tarikh():
    st.header("📅 Cari Subjek Ikut Tarikh Peperiksaan")
    st.info("Masukkan tarikh untuk lihat subjek apa yang ada pada tarikh tersebut (ikut Jadual Rasmi SPM 2026)")
    
    df_jadual = load_jadual()
    
    if df_jadual.empty:
        st.error("Jadual Rasmi tak jumpa! Pastikan sheet Jadual_Rasmi_SPM2026 ada dalam data_v1.1.xlsx")
        st.warning("Upload file JADUAL_PEPERISAAN_SPM_2026.xlsx yang Kashah bagi ke dalam data_v1.1.xlsx sebagai sheet Jadual_Rasmi_SPM2026")
        return
    
    # Clean TARIKH column
    df_jadual['TARIKH'] = df_jadual['TARIKH'].astype(str)
    tarikh_list = sorted(df_jadual['TARIKH'].dropna().unique().tolist())
    
    col1,col2 = st.columns([2,1])
    with col1:
        selected_tarikh = st.selectbox("📅 Pilih Tarikh Peperiksaan (dari Jadual Rasmi)", tarikh_list, index=0)
    with col2:
        cari_tarikh_text = st.text_input("Atau taip tarikh (contoh: 2026-12-16)", placeholder="2026-12-16")
    
    if st.button("🔍 Cari Subjek Pada Tarikh", use_container_width=True, type="primary"):
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
                st.markdown(f"- **{kod}** - {subjek} | ⏰ {masa}")
    
    with st.expander("📋 Lihat Jadual Penuh SPM 2026 (100 kertas)"):
        st.dataframe(df_jadual, use_container_width=True, height=400)
        st.download_button("📥 Download Jadual Penuh", to_excel(df_jadual), "Jadual_Penuh_SPM2026.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

def page_senarai_pusat():
    st.header("🏫 Senarai Pusat")
    df_pusat = st.session_state["data_pusat"]
    if df_pusat.empty:
        st.warning("Tiada data pusat")
        return
    st.dataframe(df_pusat, use_container_width=True, height=600)

def page_bilik_kebal():
    st.header("🔐 Bilik Kebal")
    try:
        df_bk = pd.read_excel(cari_file_excel(), sheet_name="Senarai_Bilik_Kebal", engine='openpyxl', dtype=str)
        st.dataframe(df_bk, use_container_width=True)
    except:
        st.warning("Sheet Senarai_Bilik_Kebal tiada")

# Sidebar Menu
st.sidebar.title("📚 Sistem JPN Selangor")
menu = st.sidebar.radio("Menu", [
    "Dashboard",
    "Cari Mata Pelajaran",
    "Cari Ikut Tarikh",
    "Senarai Pusat",
    "Bilik Kebal"
])

if menu == "Dashboard":
    page_dashboard()
elif menu == "Cari Mata Pelajaran":
    page_cari_mp()
elif menu == "Cari Ikut Tarikh":
    page_cari_tarikh()
elif menu == "Senarai Pusat":
    page_senarai_pusat()
elif menu == "Bilik Kebal":
    page_bilik_kebal()

st.sidebar.markdown("---")
st.sidebar.caption("SPM 2026 Selangor | Kod PPD BA besar | 60 Mata Pelajaran | 47 Bilik Kebal | 77,738 Calon")
