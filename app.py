import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Sistem JPN Selangor SPM 2026", layout="wide", page_icon="📚")

FILE_EXCEL = "data_v1.1.xlsx"

def cari_file_excel():
    for f in [FILE_EXCEL, "./data_v1.1.xlsx", "/mnt/data/data_v1.1.xlsx"]:
        if os.path.exists(f):
            return f
    return FILE_EXCEL

def to_excel(df):
    from io import BytesIO
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

def load_data_pusat():
    file_excel = cari_file_excel()
    try:
        df = pd.read_excel(file_excel, sheet_name="selenggara_pusat", engine='openpyxl', dtype=str)
        if 'Kod_PPD' in df.columns:
            df['Kod_PPD'] = df['Kod_PPD'].astype(str).str.upper()
        return df
    except:
        return pd.DataFrame()

def load_data_mp():
    file_excel = cari_file_excel()
    try:
        df = pd.read_excel(file_excel, sheet_name="MataPelajaran", engine='openpyxl', dtype=str)
        if 'Kod_PPD' in df.columns:
            df['Kod_PPD'] = df['Kod_PPD'].astype(str).str.upper()
        return df
    except:
        return pd.DataFrame()

def load_jadual():
    file_excel = cari_file_excel()
    try:
        df = pd.read_excel(file_excel, sheet_name="Jadual_Rasmi_SPM2026", engine='openpyxl', dtype=str)
        return df
    except:
        try:
            df = pd.read_excel(cari_file_excel(), sheet_name="JADUAL PEPERIKSAAN", engine='openpyxl', dtype=str)
            return df
        except:
            return pd.DataFrame()

if "data_pusat" not in st.session_state:
    st.session_state["data_pusat"] = load_data_pusat()
if "data_mp" not in st.session_state:
    st.session_state["data_mp"] = load_data_mp()

# SIDEBAR MENU - ikut screenshot Kashah
st.sidebar.title("📚 Sistem JPN Selangor SPM 2026")
st.sidebar.markdown("---")

if st.sidebar.button("📊 Dashboard", use_container_width=True):
    st.session_state["menu"] = "Dashboard"
    st.rerun()

if st.sidebar.button("📅 Jadual Waktu", use_container_width=True):
    st.session_state["menu"] = "JadualWaktu"
    st.rerun()

if st.sidebar.button("📋 Senarai Pusat", use_container_width=True):
    st.session_state["menu"] = "SenaraiPusat"
    st.rerun()

if st.sidebar.button("📚 Cari Mata Pelajaran", use_container_width=True):
    st.session_state["menu"] = "CariMP"
    st.rerun()

if st.sidebar.button("🔐 Bilik Kebal", use_container_width=True):
    st.session_state["menu"] = "BilikKebal"
    st.rerun()

if "menu" not in st.session_state:
    st.session_state["menu"] = "Dashboard"

# PAGES
def page_dashboard():
    st.header("📊 Dashboard SPM 2026 Selangor")
    df_pusat = st.session_state["data_pusat"]
    df_mp = st.session_state["data_mp"]
    if not df_pusat.empty:
        total_pusat = len(df_pusat)
        try:
            total_calon = pd.to_numeric(df_pusat['Bil_Calon_Pusat'], errors='coerce').sum()
        except:
            total_calon = 0
        c1,c2,c3 = st.columns(3)
        c1.metric("Jumlah Pusat", f"{total_pusat:,}")
        c2.metric("Jumlah Calon", f"{total_calon:,.0f}")
        c3.metric("Jumlah MP Unik", f"{df_mp['KodMP'].nunique() if not df_mp.empty else 0}")
        
        if 'Kod_PPD' in df_pusat.columns:
            st.subheader("Ikut PPD")
            try:
                df_ppd = df_pusat.groupby('Kod_PPD').agg(Bil_Pusat=('No_Pusat','count'), Jumlah_Calon=('Bil_Calon_Pusat', lambda x: pd.to_numeric(x, errors='coerce').sum())).reset_index()
                st.dataframe(df_ppd, use_container_width=True)
            except:
                pass

def page_jadual_waktu():
    st.header("📅 Jadual Waktu Peperiksaan SPM 2026")
    st.info("💡 Pilih tarikh untuk lihat subjek pada tarikh tersebut. Download akan tanya dulu sebelum download.")
    
    df_jadual = load_jadual()
    if df_jadual.empty:
        st.error("Jadual Rasmi tak jumpa! Pastikan data_v1.1.xlsx ada sheet Jadual_Rasmi_SPM2026")
        return
    
    df_jadual['TARIKH'] = df_jadual['TARIKH'].astype(str)
    tarikh_list = sorted(df_jadual['TARIKH'].dropna().unique().tolist())
    
    col1,col2 = st.columns([2,1])
    with col1:
        selected_tarikh = st.selectbox("📅 Pilih Tarikh Peperiksaan", tarikh_list, index=0, key="jadual_tarikh")
    with col2:
        cari_text = st.text_input("Atau taip tarikh (2026-12-16)", placeholder="2026-12-16", key="jadual_text")
    
    if st.button("🔍 Cari Subjek Pada Tarikh", use_container_width=True, type="primary"):
        if cari_text:
            df_filter = df_jadual[df_jadual['TARIKH'].astype(str).str.contains(cari_text, case=False, na=False)]
            tarikh_display = cari_text
        else:
            df_filter = df_jadual[df_jadual['TARIKH'] == selected_tarikh]
            tarikh_display = selected_tarikh
        
        if df_filter.empty:
            st.warning(f"Tiada subjek pada tarikh {tarikh_display}")
        else:
            st.success(f"✅ Jumpa {len(df_filter)} kertas pada {tarikh_display}")
            cols_show = [c for c in ['HARI','TARIKH','MASA MENJAWAB','KOD MATA PELAJARAN','KOD KERTAS','MATA PELAJARAN'] if c in df_filter.columns]
            st.dataframe(df_filter[cols_show], use_container_width=True)
            
            st.subheader(f"📚 Ringkasan {tarikh_display}")
            for _, row in df_filter.iterrows():
                kod = row.get('KOD KERTAS','') or row.get('KOD MATA PELAJARAN','')
                subjek = row.get('MATA PELAJARAN','')
                masa = row.get('MASA MENJAWAB','')
                st.markdown(f"- **{kod}** - {subjek} | ⏰ {masa}")
    
    st.markdown("---")
    st.subheader("📋 Jadual Penuh SPM 2026")
    
    with st.expander("Lihat Jadual Penuh (100 kertas)", expanded=False):
        st.dataframe(df_jadual, use_container_width=True, height=400)
        
        st.markdown("### 📥 Nak download Jadual Penuh?")
        st.caption("Sistem tidak akan auto-download. Tick checkbox dulu untuk download.")
        
        confirm = st.checkbox("✅ Ya, saya nak download Jadual Penuh SPM 2026", key="confirm_jadual")
        
        if confirm:
            st.warning("⚠️ Anda akan download file Excel Jadual Penuh SPM 2026")
            col_yes, col_no = st.columns(2)
            with col_yes:
                st.download_button(
                    "📥 Ya, Download Sekarang", 
                    to_excel(df_jadual), 
                    "Jadual_Penuh_SPM2026.xlsx", 
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 
                    key="dl_jadual_yes",
                    type="primary",
                    use_container_width=True
                )
            with col_no:
                if st.button("❌ Batal", use_container_width=True):
                    st.session_state["confirm_jadual"] = False
                    st.rerun()
        else:
            st.info("☝️ Tick checkbox di atas jika nak download. Sistem tidak auto-download.")

def page_senarai_pusat():
    st.header("📋 Senarai Pusat Peperiksaan")
    df_pusat = st.session_state["data_pusat"]
    if df_pusat.empty:
        st.warning("Tiada data pusat")
        return
    cols = [c for c in ["Kod_PPD","No_Pusat","Nama_Pusat","Bil_Calon_Pusat","Kod_Bilik_Kebal","Nama_Bilik_Kebal"] if c in df_pusat.columns]
    st.dataframe(df_pusat[cols], use_container_width=True, height=600)
    st.download_button("📥 Download Senarai Pusat", to_excel(df_pusat[cols]), "Senarai_Pusat.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

def page_cari_mp():
    st.header("📚 Carian Mata Pelajaran Mengikut Pusat")
    df_mp = st.session_state["data_mp"]
    if df_mp.empty:
        st.warning("Data MP kosong!")
        return
    
    col1,col2,col3 = st.columns(3)
    with col1:
        cari_kod = st.text_input("1. Kod Mata Pelajaran", placeholder="Contoh: 4541 KIMIA, 4531 FIZIK", key="cari_kod")
    with col2:
        cari_nama = st.text_input("2. Nama Mata Pelajaran", placeholder="Contoh: KIMIA, FIZIK, Tamil", key="cari_nama")
    with col3:
        kertas_opts = ["Semua"] + sorted(df_mp['Kertas'].dropna().unique().tolist()) if 'Kertas' in df_mp.columns else ["Semua"]
        cari_kertas = st.selectbox("3. Kertas", kertas_opts, key="cari_kertas")
    
    if st.button("🔍 Cari Sekarang", use_container_width=True, type="primary"):
        df_filter = df_mp.copy()
        if cari_kod:
            df_filter = df_filter[df_filter['KodMP'].astype(str).str.contains(cari_kod, case=False, na=False)]
        if cari_nama:
            mask = df_filter['NamaMP'].astype(str).str.contains(cari_nama, case=False, na=False)
            if 'NamaMP_Sebenar' in df_filter.columns:
                mask = mask | df_filter['NamaMP_Sebenar'].astype(str).str.contains(cari_nama, case=False, na=False)
            df_filter = df_filter[mask]
        if cari_kertas != "Semua" and 'Kertas' in df_filter.columns:
            df_filter = df_filter[df_filter['Kertas'].astype(str) == str(cari_kertas)]
        
        if df_filter.empty:
            st.warning("❌ Tiada pusat yang menawarkan mata pelajaran tersebut")
            st.info("💡 Tips: 4541=KIMIA, 4531=FIZIK, 9217=Tamil, 9216=Cina, 2216=Melayu, 2206=Inggeris, 5303=Turath")
        else:
            jumlah_rekod = len(df_filter)
            jumlah_pusat = df_filter.drop_duplicates(subset=["No_Pusat"]).shape[0] if "No_Pusat" in df_filter.columns else jumlah_rekod
            st.success(f"✅ Jumpa {jumlah_rekod} rekod | {jumlah_pusat} pusat")
            
            c1,c2 = st.columns(2)
            c1.metric("Jumlah Rekod MP", f"{jumlah_rekod:,}")
            c2.metric("Jumlah Pusat", f"{jumlah_pusat:,} pusat")
            
            cols_show = [c for c in ["Kod_PPD","No_Pusat","Nama_Pusat","KodMP","NamaMP","Kertas","Bil_Calon","Bil_Naskah","Kod_Bilik_Kebal","Nama_Bilik_Kebal"] if c in df_filter.columns]
            st.dataframe(df_filter[cols_show].drop_duplicates(), use_container_width=True, height=500)

def page_bilik_kebal():
    st.header("🔐 Senarai Bilik Kebal")
    try:
        df_bk = pd.read_excel(cari_file_excel(), sheet_name="Senarai_Bilik_Kebal", engine='openpyxl', dtype=str)
        st.dataframe(df_bk, use_container_width=True)
    except Exception as e:
        st.warning(f"Sheet Senarai_Bilik_Kebal tiada: {e}")

# ROUTING
menu = st.session_state.get("menu", "Dashboard")
if menu == "Dashboard":
    page_dashboard()
elif menu == "JadualWaktu":
    page_jadual_waktu()
elif menu == "SenaraiPusat":
    page_senarai_pusat()
elif menu == "CariMP":
    page_cari_mp()
elif menu == "BilikKebal":
    page_bilik_kebal()

st.sidebar.markdown("---")
st.sidebar.caption("SPM 2026 Selangor | 4541=KIMIA 4531=FIZIK 9217=Tamil | 504 Pusat | 77,738 Calon")
