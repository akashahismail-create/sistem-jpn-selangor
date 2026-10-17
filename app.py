import streamlit as st
from pathlib import Path
import csv
import re
from collections import Counter
import tempfile

st.set_page_config(page_title="Sistem Analisis Kehadiran Calon - JPN Selangor", layout="wide", initial_sidebar_state="collapsed")

FOLDER_DESKTOP = Path.home() / "Desktop" / "data_kehadiran_calon"
TEMP_FOLDER = Path(tempfile.gettempdir()) / "data_kehadiran_calon_jpn"
TEMP_FOLDER.mkdir(exist_ok=True)

JENIS_CALON = {"A": "Sekolah (SBK/SABK)", "B": "Agensi Kerajaan", "C": "Agama Rakyat", "D": "Sekolah Swasta", "E": "Persendirian"}

def parse_angka(angka):
    angka = str(angka).strip().upper()
    m = re.match(r'^([A-Z]{2})(\d{3})([A-Z])(\d{3})$', angka)
    if m:
        return {"daerah": m.group(1), "pusat": m.group(2), "jenis": m.group(3)}
    return {"daerah": "", "pusat": "", "jenis": "?"}

def baca_csv(file_path):
    total=0; hadir=0; th=0
    asing=Counter(); ah=Counter(); at=Counter()
    rd={}; rl=[]
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for row in reader:
            angka = str(row.get('Angka Giliran','')).strip().upper()
            if not angka: continue
            total+=1
            p = parse_angka(angka)
            jenis = p['jenis']
            row['Jenis_Huruf'] = jenis
            row['Jenis_Label'] = JENIS_CALON.get(jenis, jenis)
            row['Daerah_Kod'] = p['daerah']
            asing[jenis]+=1
            status = row.get('Status Kehadiran','').strip()
            if status == 'Hadir': hadir+=1; ah[jenis]+=1
            elif status == 'Tidak Hadir': th+=1; at[jenis]+=1
            rd[angka]=row; rl.append(row)
    peratus = (hadir/total*100) if total>0 else 0
    return total, hadir, th, peratus, asing, ah, at, rd, rl

SUBJEK_LENGKAP = {
    "1103 - Bahasa Melayu (4 Kertas)": {"kertas": [{"key": "1103/1", "file": "1103_1", "nama": "BM K1 Bertulis"}, {"key": "1103/2", "file": "1103_2", "nama": "BM K2 Bertulis"}, {"key": "1103/3", "file": "1103_3", "nama": "BM K3 Bertutur"}, {"key": "1103/4", "file": "1103_4", "nama": "BM K4 Mendengar"}]},
    "1119 - Bahasa Inggeris (4 Kertas)": {"kertas": [{"key": "1119/1", "file": "1119_1", "nama": "BI K1"}, {"key": "1119/2", "file": "1119_2", "nama": "BI K2"}, {"key": "1119/3", "file": "1119_3", "nama": "BI K3 Bertutur"}, {"key": "1119/4", "file": "1119_4", "nama": "BI K4 Mendengar"}]},
    "1223 - Pendidikan Islam": {"kertas": [{"key": "1223/1", "file": "1223_1"}, {"key": "1223/2", "file": "1223_2"}]},
    "1225 - Pendidikan Moral": {"kertas": [{"key": "1225", "file": "1225"}]},
    "1249 - Sejarah": {"kertas": [{"key": "1249/1", "file": "1249_1"}, {"key": "1249/2", "file": "1249_2"}]},
    "1449 - Matematik": {"kertas": [{"key": "1449/1", "file": "1449_1"}, {"key": "1449/2", "file": "1449_2"}]},
    "1511 - Sains": {"kertas": [{"key": "1511/1", "file": "1511_1"}, {"key": "1511/2", "file": "1511_2"}]},
    "2361 - Bahasa Arab": {"kertas": [{"key": "2361/1", "file": "2361_1"}]},
    "2611 - Seni Visual": {"kertas": [{"key": "2611/1", "file": "2611_1"}, {"key": "2611/2", "file": "2611_2"}]},
    "3729 - Pertanian": {"kertas": [{"key": "3729/1", "file": "3729_1"}]},
    "3759 - Lukisan Kejuruteraan": {"kertas": [{"key": "3759/1", "file": "3759_1"}]},
    "3763 - Reka Cipta": {"kertas": [{"key": "3763/1", "file": "3763_1"}]},
    "3766 - Perniagaan": {"kertas": [{"key": "3766/1", "file": "3766_1"}, {"key": "3766/2", "file": "3766_2"}, {"key": "3766/4", "file": "3766_4"}]},
    "3767 - Ekonomi": {"kertas": [{"key": "3767/1", "file": "3767_1"}, {"key": "3767/2", "file": "3767_2"}]},
    "3769 - Sains Rumah Tangga": {"kertas": [{"key": "3769/1", "file": "3769_1"}]},
    "3771 - Grafik Teknikal": {"kertas": [{"key": "3771/1", "file": "3771_1"}]},
    "4531 - Fizik": {"kertas": [{"key": "4531/1", "file": "4531_1"}, {"key": "4531/2", "file": "4531_2"}, {"key": "4531/3", "file": "4531_3"}]},
    "4541 - Kimia": {"kertas": [{"key": "4541/3", "file": "4541_3"}, {"key": "4541/1", "file": "4541_1"}, {"key": "4541/2", "file": "4541_2"}]},
    "4551 - Biologi": {"kertas": [{"key": "4551/1", "file": "4551_1"}, {"key": "4551/2", "file": "4551_2"}, {"key": "4551/3", "file": "4551_3"}]},
    "4561 - Sains Tambahan": {"kertas": [{"key": "4561/3", "file": "4561_3"}]},
    "5226 - Tasawwur Islam": {"kertas": [{"key": "5226", "file": "5226"}]},
    "5302 - Maharat Quran": {"kertas": [{"key": "5302/2", "file": "5302_2"}]},
    "5402 - Al-Syariah": {"kertas": [{"key": "5402/1", "file": "5402_1"}]},
    "5403 - Al-Lughah": {"kertas": [{"key": "5403/1", "file": "5403_1"}]},
    "5404 - Manahij": {"kertas": [{"key": "5404/1", "file": "5404_1"}]},
    "6351 - Bahasa Cina": {"kertas": [{"key": "6351/1", "file": "6351_1"}]},
    "7101 - MPV": {"kertas": [{"key": "7101/1", "file": "7101_1"}]},
    "3472 - Math Tambahan": {"kertas": [{"key": "3472/1", "file": "3472_1"}, {"key": "3472/2", "file": "3472_2"}]},
    "3756 - Prinsip Perakaunan": {"kertas": [{"key": "3756/1", "file": "3756_1"}, {"key": "3756/4", "file": "3756_4"}]},
}

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'stats_all' not in st.session_state:
    st.session_state.stats_all = {}
if 'menu_utama' not in st.session_state:
    st.session_state['menu_utama'] = "📚 Semua Subjek"
if 'filter_jenis' not in st.session_state:
    st.session_state['filter_jenis'] = None

def get_active_folder():
    # FIX: Check TEMP dulu, baru Desktop - sebab di Streamlit Cloud Desktop tak wujud
    temp_files = list(TEMP_FOLDER.glob("*.csv")) if TEMP_FOLDER.exists() else []
    if len(temp_files) > 0:
        return TEMP_FOLDER, f"UPLOAD (Streamlit Cloud) - {len(temp_files)} file"
    desktop_files = list(FOLDER_DESKTOP.glob("*.csv")) if FOLDER_DESKTOP.exists() else []
    if len(desktop_files) > 0:
        return FOLDER_DESKTOP, f"DESKTOP - {len(desktop_files)} file"
    # Kalau temp folder wujud tapi kosong, guna temp untuk upload
    if TEMP_FOLDER.exists():
        return TEMP_FOLDER, "UPLOAD (Streamlit Cloud) - Sedia Upload"
    return FOLDER_DESKTOP, "DESKTOP (Belum Ada Data)"

if not st.session_state['logged_in']:
    st.markdown("""
    <div style="text-align: center; background: linear-gradient(90deg, #0d47a1, #1976d2); color: white; padding: 30px; border-radius: 15px; margin-bottom: 20px;">
        <h1>📊 SISTEM ANALISIS KEHADIRAN CALON</h1>
        <h3>Sektor Pentaksiran dan Peperiksaan</h3>
        <h4>Jabatan Pendidikan Negeri Selangor</h4>
        <p>SPM 2026 - 27 Subjek, 43 Kertas - Data di DESKTOP</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("### 🔐 Log Masuk Sistem")
        id_input = st.text_input("ID Pengguna:", placeholder="Masukkan ID")
        pass_input = st.text_input("Password:", type="password", placeholder="Masukkan Password")
        if st.button("🔓 LOG MASUK", type="primary", use_container_width=True):
            if id_input == "jpn" and pass_input == "2026":
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("❌ ID atau Password salah! ID: jpn, Password: 2026")
        st.info("ID: jpn | Password: 2026 | Data di Desktop/data_kehadiran_calon")
    st.stop()

FOLDER, SUMBER = get_active_folder()

st.markdown(f"""
<div style="background: linear-gradient(90deg, #0d47a1, #1976d2); color:white; padding:15px; border-radius:10px; display:flex; justify-content:space-between; align-items:center;">
<div>
<h3 style="margin:0; color:white;">📊 SISTEM ANALISIS KEHADIRAN CALON</h3>
<p style="margin:0; color:#bbdefb;">Sektor Pentaksiran dan Peperiksaan | JPN Selangor | {SUMBER}</p>
</div>
<div style="text-align:right;">
<p style="margin:0; color:white;">👤 JPN (jpn)</p>
<p style="margin:0; color:#bbdefb; font-size:12px;">{SUMBER}</p>
</div>
</div>
""", unsafe_allow_html=True)

col_logout1, col_logout2 = st.columns([6,1])
with col_logout2:
    if st.button("🔒 Log Keluar", use_container_width=True):
        st.session_state['logged_in'] = False
        st.rerun()

# ===== UPLOADER - FIXED =====
# Kalau Desktop kosong dan Temp pun kosong, atau kita di Cloud, tunjuk uploader
desktop_has = len(list(FOLDER_DESKTOP.glob("*.csv"))) if FOLDER_DESKTOP.exists() else []
temp_has = len(list(TEMP_FOLDER.glob("*.csv"))) if TEMP_FOLDER.exists() else []

if temp_has == 0 and desktop_has == 0:
    st.warning(f"⚠️ Data tidak ditemui. Sila upload CSV dari Desktop/data_kehadiran_calon")
    st.markdown("### 📤 Upload Data dari Desktop (Data Tidak Disimpan di GitHub)")
    uploaded_files = st.file_uploader("Pilih file CSV (1103_1.csv, dll) - boleh pilih banyak file terus", type=["csv"], accept_multiple_files=True)
    if uploaded_files:
        for uf in uploaded_files:
            save_path = TEMP_FOLDER / uf.name
            with open(save_path, "wb") as f:
                f.write(uf.getbuffer())
        st.success(f"✅ {len(uploaded_files)} file berjaya diupload! Sila tunggu refresh...")
        st.rerun()
else:
    # Dah ada data, tunjuk info dan bagi option upload lagi kalau nak tambah
    if "UPLOAD" in SUMBER:
        st.success(f"✅ {SUMBER} | Folder: {TEMP_FOLDER}")
        with st.expander("📤 Tambah / Ganti file CSV"):
            uploaded_files = st.file_uploader("Upload lagi file CSV dari Desktop", type=["csv"], accept_multiple_files=True, key="tambah")
            if uploaded_files:
                for uf in uploaded_files:
                    save_path = TEMP_FOLDER / uf.name
                    with open(save_path, "wb") as f:
                        f.write(uf.getbuffer())
                st.success(f"✅ {len(uploaded_files)} file diupload!")
                st.rerun()
    else:
        st.success(f"✅ {SUMBER} | Folder: {FOLDER}")

# Refresh folder selepas upload
FOLDER, SUMBER = get_active_folder()

left_menu, right_content = st.columns([1.2, 3.8])

with left_menu:
    st.markdown("### 📋 MENU UTAMA")
    if st.button("📚 Semua Subjek\n27 Subjek", use_container_width=True, type="primary" if st.session_state['menu_utama']=="📚 Semua Subjek" else "secondary"):
        st.session_state['menu_utama'] = "📚 Semua Subjek"; st.rerun()
    if st.button("⚖️ Perbandingan\n3 Butang", use_container_width=True, type="primary" if st.session_state['menu_utama']=="⚖️ Perbandingan" else "secondary"):
        st.session_state['menu_utama'] = "⚖️ Perbandingan"; st.rerun()
    st.markdown("---")
    st.markdown("### 🎓 JENIS CALON")
    if st.button("🌐 SEMUA", use_container_width=True, type="primary" if st.session_state['filter_jenis'] is None else "secondary"):
        st.session_state['filter_jenis']=None; st.rerun()
    for h,l in JENIS_CALON.items():
        if st.button(f"{h} - {l}", use_container_width=True, type="primary" if st.session_state['filter_jenis']==h else "secondary", key=f"jenis_{h}"):
            st.session_state['filter_jenis']=h; st.rerun()
    st.markdown("---")
    st.write(f"📂 {SUMBER}")
    st.write(f"📁 {FOLDER}")
    if FOLDER.exists():
        files = sorted([f.name for f in FOLDER.glob("*.csv")])
        if files:
            st.success(f"📂 {len(files)} file")
            for f in files[:15]:
                st.write(f"📄 {f}")
        else:
            st.warning("Tiada CSV"); files=[]
    else:
        st.error(f"Folder tak wujud"); files=[]

with right_content:
    filter_huruf = st.session_state['filter_jenis']
    if filter_huruf:
        st.warning(f"🔍 Filter: Jenis {filter_huruf} - {JENIS_CALON[filter_huruf]} | {SUMBER}")
    else:
        st.info(f"🌐 SEMUA JENIS | {SUMBER} | {len(files)} file CSV")
    
    if not files:
        st.error("❌ Tiada file CSV. Sila upload di atas.")
        st.stop()
    
    if st.session_state['menu_utama'] == "📚 Semua Subjek":
        st.header(f"📚 Semua Subjek - {len(files)} file ada")
        selected_subjek = st.selectbox("Pilih Mata Pelajaran (27 subjek):", list(SUBJEK_LENGKAP.keys()), index=0)
        kertas_list = SUBJEK_LENGKAP[selected_subjek]["kertas"]
        st.write(f"**{selected_subjek}** - {len(kertas_list)} kertas")
        tabs = st.tabs([f"{k['key']}" for k in kertas_list])
        for idx, tab in enumerate(tabs):
            with tab:
                k_info = kertas_list[idx]
                file_hint = k_info["file"]
                key = k_info["key"]
                st.write(f"**{key} - {k_info.get('nama','')}** - File: {file_hint}.csv")
                found = FOLDER / f"{file_hint}.csv" if (FOLDER / f"{file_hint}.csv").exists() else None
                c1,c2 = st.columns([3,1])
                with c1:
                    if found:
                        st.success(f"✅ {found.name} ada di {SUMBER}")
                    else:
                        st.warning(f"Belum ada {file_hint}.csv")
                with c2:
                    if st.button(f"📂 BACA {key}", key=f"baca_{key}_{idx}", type="primary", use_container_width=True, disabled=found is None):
                        if found:
                            total, hadir, th, peratus, asing, ah, at, rd, rl = baca_csv(found)
                            st.session_state.stats_all[key] = {"total": total, "hadir": hadir, "th": th, "peratus": peratus, "asing": asing, "ah": ah, "at": at, "rd": rd, "rl": rl, "file_hint": file_hint}
                            st.rerun()
                stats = st.session_state.stats_all.get(key)
                if stats:
                    rows_filtered = stats['rl']
                    if filter_huruf:
                        rows_filtered = [r for r in rows_filtered if r['Jenis_Huruf']==filter_huruf]
                        total_f = len(rows_filtered); hadir_f = sum(1 for r in rows_filtered if r.get('Status Kehadiran')=='Hadir'); th_f = total_f-hadir_f; per_f = (hadir_f/total_f*100) if total_f>0 else 0
                    else:
                        total_f = stats['total']; hadir_f = stats['hadir']; th_f = stats['th']; per_f = stats['peratus']
                    m1,m2,m3,m4 = st.columns(4)
                    m1.metric(f"Jumlah ({filter_huruf if filter_huruf else 'SEMUA'})", f"{total_f:,}")
                    m2.metric("Hadir", f"{hadir_f:,}")
                    m3.metric("TH", f"{th_f:,}")
                    m4.metric("%", f"{per_f:.1f}%")
                    st.markdown(f"#### 📊 Asingan A-E")
                    table=[]
                    for h in ["A","B","C","D","E"]:
                        if h in stats['asing']:
                            table.append({"Huruf": h, "Jenis": JENIS_CALON[h], "Jumlah": stats['asing'][h], "Hadir": stats['ah'].get(h,0), "TH": stats['at'].get(h,0), "Aktif": "👉" if filter_huruf==h else ""})
                    st.dataframe(table, use_container_width=True)
                    st.markdown(f"#### 📋 Senarai {filter_huruf if filter_huruf else 'SEMUA'} ({len(rows_filtered)} calon)")
                    if rows_filtered:
                        disp=[{"Angka": r.get('Angka Giliran'), "Nama": r.get('Nama',''), "Daerah": r.get('Daerah_Kod'), "Jenis": r.get('Jenis_Huruf'), "Status": r.get('Status Kehadiran'), "Pusat": r.get('Nama Pusat','')[:35]} for r in rows_filtered[:500]]
                        st.dataframe(disp, use_container_width=True)
    else:
        st.header("⚖️ Perbandingan 2 Kertas")
        if len(files) < 2:
            st.warning("Perlu upload sekurang-kurangnya 2 file CSV untuk perbandingan")
        else:
            col1, col2 = st.columns(2)
            with col1:
                kertas_a = st.selectbox("Kertas A:", files, key="ka")
            with col2:
                kertas_b = st.selectbox("Kertas B:", files, index=1 if len(files)>1 else 0, key="kb")
            if st.button("📊 BANDING SEKARANG", type="primary", use_container_width=True):
                if kertas_a and kertas_b and kertas_a != kertas_b:
                    _,_,_,_,_,_,_,data_a,_ = baca_csv(FOLDER / kertas_a)
                    _,_,_,_,_,_,_,data_b,_ = baca_csv(FOLDER / kertas_b)
                    set_a=set(data_a.keys()); set_b=set(data_b.keys()); sama=set_a & set_b
                    if filter_huruf:
                        sama={angka for angka in sama if data_a.get(angka, {}).get('Jenis_Huruf')==filter_huruf}
                    hadir2=[]; hadir1=[]; ha_th=[]; th_ha=[]; th2=[]
                    for angka in sama:
                        sa=data_a[angka].get('Status Kehadiran','').strip()
                        sb=data_b[angka].get('Status Kehadiran','').strip()
                        if sa=='Hadir' and sb=='Hadir': hadir2.append(angka)
                        elif sa=='Tidak Hadir' and sb=='Tidak Hadir': th2.append(angka)
                        elif sa=='Hadir' and sb=='Tidak Hadir': ha_th.append(angka); hadir1.append(angka)
                        elif sa=='Tidak Hadir' and sb=='Hadir': th_ha.append(angka); hadir1.append(angka)
                    st.session_state['b']={"ka": kertas_a, "kb": kertas_b, "da": data_a, "db": data_b, "hadir2": hadir2, "hadir1": hadir1, "ha_th": ha_th, "th_ha": th_ha, "th2": th2, "sama": sama}
            if 'b' in st.session_state:
                b=st.session_state['b']
                st.subheader(f"{b['ka']} vs {b['kb']} - {len(b['sama'])} calon sama")
                c1,c2,c3=st.columns(3)
                with c1:
                    if st.button(f"✅ HADIR KEDUA-DUA\n{len(b['hadir2'])}", key="btn_h2", use_container_width=True, type="primary"):
                        st.session_state['pilihan']="hadir2"
                with c2:
                    if st.button(f"⚠️ HADIR 1 & TH 1\n{len(b['hadir1'])}", key="btn_h1", use_container_width=True):
                        st.session_state['pilihan']="hadir1"
                with c3:
                    if st.button(f"❌ TH KEDUA-DUA\n{len(b['th2'])}", key="btn_t2", use_container_width=True):
                        st.session_state['pilihan']="th2"
                d1,d2=st.columns(2)
                with d1:
                    if st.button(f"➡️ Hadir {b['ka']} TH {b['kb']} ({len(b['ha_th'])})", key="btn_a", use_container_width=True):
                        st.session_state['pilihan']="ha_th"
                with d2:
                    if st.button(f"⬅️ TH {b['ka']} Hadir {b['kb']} ({len(b['th_ha'])})", key="btn_b", use_container_width=True):
                        st.session_state['pilihan']="th_ha"
                if 'pilihan' in st.session_state:
                    p=st.session_state['pilihan']
                    mapping={"hadir2": b['hadir2'], "hadir1": b['hadir1'], "th2": b['th2'], "ha_th": b['ha_th'], "th_ha": b['th_ha']}
                    senarai=mapping.get(p, [])
                    st.markdown(f"### {p} - {len(senarai)} calon")
                    if senarai:
                        rows=[{"Angka": a, "Nama": b['da'].get(a, {}).get('Nama',''), "Daerah": b['da'].get(a, {}).get('Daerah_Kod',''), "Jenis": b['da'].get(a, {}).get('Jenis_Huruf',''), f"Status {b['ka']}": b['da'].get(a, {}).get('Status Kehadiran',''), f"Status {b['kb']}": b['db'].get(a, {}).get('Status Kehadiran',''), "Pusat": b['da'].get(a, {}).get('Nama Pusat','')[:35]} for a in senarai[:1000]]
                        st.dataframe(rows, use_container_width=True)

st.caption(f"FIXED - Data: {FOLDER} | Sumber: {SUMBER} | Desktop: {FOLDER_DESKTOP} | Temp: {TEMP_FOLDER}")
