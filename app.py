import streamlit as st
import base64
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from io import BytesIO

st.set_page_config(page_title="JPN Selangor", layout="wide")

FILE_NOTIS="pemberitahuan.json"
DEFAULT_NOTIS="📢 MAKLUMAN: Data SPM 2025 sedang dikemaskini"
PASSWORD_DELETE="akashah"
LINK_GITHUB_REPO="https://github.com/akashahismail-create/sistem-jpn-selangor"
FILE_EXCEL="data_v1.1.xlsx"
SHEET_PUSAT="selenggara_pusat"
SHEET_MP="MataPelajaran"
COLUMNS_PUSAT=["Kod_PPD","No_Pusat","Nama_Pusat","Bil_Calon_Pusat","Nama_Bilik_Kebal","Dikemaskini_Oleh","Tarikh_Kemaskini"]
COLUMNS_MP=["Kod_PPD","No_Pusat","Nama_Pusat","KodMP","NamaMP","Kertas","Tarikh"]
FILE_CALON_JSON="data_calon.json"
KOD_PPD={"Petaling Perdana":"BH","Petaling Utama":"BK","Hulu Langat":"BD","Gombak":"BG","Klang":"BA","Kuala Langat":"BB","Kuala Selangor":"BC","Hulu Selangor":"BE","Sabak Bernam":"BF","Sepang":"BJ"}
USERS={"admin":{"password":"jpn","role":"Admin"},"bh":{"password":"bh","role":"PPD","daerah":"Petaling Perdana"},"bk":{"password":"bk","role":"PPD","daerah":"Petaling Utama"},"bd":{"password":"bd","role":"PPD","daerah":"Hulu Langat"},"bg":{"password":"bg","role":"PPD","daerah":"Gombak"},"ba":{"password":"ba","role":"PPD","daerah":"Klang"},"bb":{"password":"bb","role":"PPD","daerah":"Kuala Langat"},"bc":{"password":"bc","role":"PPD","daerah":"Kuala Selangor"},"be":{"password":"be","role":"PPD","daerah":"Hulu Selangor"},"bf":{"password":"bf","role":"PPD","daerah":"Sabak Bernam"},"bj":{"password":"bj","role":"PPD","daerah":"Sepang"}}
JENIS_CALON=["Semua Jenis","A-Sekolah Kerajaan","B-Sekolah Agensi","C-Sekolah Bantuan Kerajaan","D-Sekolah Swasta","E-Calon Persendirian"]
JENIS_PETUGAS=["Semua Jawatan","Penyelia Kawasan","Ketua Pengawas","Timbalan Ketua Pengawas","Pengawas","Pengemas Bilik","Sukarelawan"]
def load_notis():
    if os.path.exists(FILE_NOTIS):
        try:
            with open(FILE_NOTIS,"r",encoding="utf-8") as f:
                d=json.load(f); return {"teks":d.get("teks",DEFAULT_NOTIS),"image":d.get("image")}
        except: return {"teks":DEFAULT_NOTIS,"image":None}
    else: return {"teks":DEFAULT_NOTIS,"image":None}
def simpan_notis(teks,image_b64=None):
    with open(FILE_NOTIS,"w",encoding="utf-8") as f:
        json.dump({"teks":teks,"image":image_b64,"dikemaskini":datetime.now().strftime("%Y-%m-%d %H:%M")},f,ensure_ascii=False,indent=2)
data_notis=load_notis()
teks_notis=data_notis.get("teks","")
img_notis=data_notis.get("image")
if teks_notis.strip()!="" or img_notis:
    img_tag=f'<img src="data:image/png;base64,{img_notis}" style="height:28px;vertical-align:middle;margin-right:12px;border-radius:4px;background:white;">' if img_notis else ""
    st.markdown(f'<div style="background:linear-gradient(90deg,#B71C1C 0%,#C62828 100%);border:2px solid #FFD700;border-radius:10px;padding:8px 0px;margin-bottom:12px;"><marquee scrollamount="7" style="color:#FFEB3B;font-weight:bold;font-size:15px;">{img_tag} {teks_notis} • {teks_notis}</marquee></div>',unsafe_allow_html=True)

def load_data_calon():
    if os.path.exists(FILE_CALON_JSON):
        try:
            with open(FILE_CALON_JSON,"r") as f: return json.load(f)
        except: return DATA_ASAL
    else: return DATA_ASAL
def simpan_data_calon(data):
    with open(FILE_CALON_JSON,"w") as f: json.dump(data,f,indent=2)
    st.session_state["data_calon"]=data
def load_data_pusat():
    if os.path.exists(FILE_EXCEL):
        try: return pd.read_excel(FILE_EXCEL,sheet_name=SHEET_PUSAT,engine='openpyxl',dtype=str)
        except: return pd.DataFrame(columns=COLUMNS_PUSAT)
    else: return pd.DataFrame(columns=COLUMNS_PUSAT)
def load_data_mp():
    if os.path.exists(FILE_EXCEL):
        try: return pd.read_excel(FILE_EXCEL,sheet_name=SHEET_MP,engine='openpyxl',dtype=str)
        except: return pd.DataFrame(columns=COLUMNS_MP)
    else: return pd.DataFrame(columns=COLUMNS_MP)
def to_excel(df):
    output=BytesIO()
    with pd.ExcelWriter(output,engine='openpyxl') as writer: df.to_excel(writer,index=False)
    return output.getvalue()
def simpan_ke_excel():
    with pd.ExcelWriter(FILE_EXCEL,engine='openpyxl',mode='w') as writer:
        st.session_state["data_pusat"].to_excel(writer,sheet_name=SHEET_PUSAT,index=False)
        st.session_state["data_mp"].to_excel(writer,sheet_name=SHEET_MP,index=False)
def simpan_data_pusat(kod_ppd,no_pusat,nama_pusat,bil_calon,nama_kebal,dikemaskini_oleh):
    df=st.session_state["data_pusat"]
    df=df[df['No_Pusat']!=no_pusat]
    data_baru=pd.DataFrame([{'Kod_PPD':kod_ppd,'No_Pusat':no_pusat,'Nama_Pusat':nama_pusat,'Bil_Calon_Pusat':bil_calon,'Nama_Bilik_Kebal':nama_kebal,'Dikemaskini_Oleh':dikemaskini_oleh,'Tarikh_Kemaskini':datetime.now().strftime("%Y-%m-%d %H:%M")}])
    st.session_state["data_pusat"]=pd.concat([df,data_baru],ignore_index=True)
    simpan_ke_excel()

if "data_calon" not in st.session_state: st.session_state["data_calon"]=load_data_calon()
if "data_pusat" not in st.session_state: st.session_state["data_pusat"]=load_data_pusat()
if "data_mp" not in st.session_state: st.session_state["data_mp"]=load_data_mp()
if "editor_login" not in st.session_state: st.session_state["editor_login"]=False
if "show_editor" not in st.session_state: st.session_state["show_editor"]=False
if "menu" not in st.session_state: st.session_state["menu"]="Dashboard"

def login_editor():
    with st.form("login_form"):
        st.markdown("#### 🔒 Log Masuk")
        username=st.text_input("Nama Pengguna",key="user_login")
        password=st.text_input("Kata Laluan",type="password",key="pass_login")
        if st.form_submit_button("Log Masuk",use_container_width=True,type="primary"):
            uname=username.lower().strip()
            if uname in USERS and USERS[uname]["password"]==password:
                st.session_state["editor_login"]=True
                st.session_state["username"]=uname
                st.session_state["role"]=USERS[uname]["role"]
                if USERS[uname]["role"]=="PPD":
                    st.session_state["daerah_ppd"]=USERS[uname]["daerah"]
                    st.session_state["kod_ppd"]=KOD_PPD[USERS[uname]["daerah"]]
                st.success(f"Login {uname}"); st.rerun()
            else: st.error("Salah!")

def page_selenggara_pusat():
    st.header("⚙️ Selenggara Data")
    if not st.session_state.get("editor_login",False):
        st.warning("Login dulu"); return
    role=st.session_state.get("role","")
    if role=="Admin":
        tab_pusat,tab_mp,tab_calon,tab_notis,tab_db=st.tabs(["🏫 Pusat","📚 MP","👥 Calon","📢 Notis","💾 Urus File + Github"])
    else:
        tab_pusat,tab_calon=st.tabs(["🏫 Pusat","👥 Calon"])
        tab_mp=None; tab_notis=None; tab_db=None
    with tab_pusat:
        if role=="Admin":
            pilihan_ppd=st.selectbox("Pilih PPD",list(KOD_PPD.values()))
        else:
            pilihan_ppd=st.session_state["kod_ppd"]
            st.info(f"PPD: {st.session_state['daerah_ppd']} - {pilihan_ppd}")
        with st.form("form_pusat"):
            c1,c2=st.columns(2)
            with c1:
                no_pusat=st.text_input("No Pusat *")
                nama_pusat=st.text_input("Nama Pusat *")
            with c2:
                bil_calon=st.number_input("Bil Calon",min_value=0,step=1)
                nama_kebal=st.text_input("Bilik Kebal")
            if st.form_submit_button("💾 Simpan",type="primary",use_container_width=True):
                if no_pusat and nama_pusat:
                    simpan_data_pusat(pilihan_ppd,no_pusat,nama_pusat,bil_calon,nama_kebal,st.session_state["username"])
                    st.success("Disimpan"); st.rerun()
        df_tunjuk=st.session_state["data_pusat"][st.session_state["data_pusat"]['Kod_PPD']==pilihan_ppd]
        edited_df=st.data_editor(df_tunjuk,use_container_width=True,num_rows="dynamic",key=f"ed_{pilihan_ppd}")
        if st.button("💾 SIMPAN EDIT",type="primary",use_container_width=True):
            if not edited_df.empty:
                edited_df['Dikemaskini_Oleh']=st.session_state["username"]
                edited_df['Tarikh_Kemaskini']=datetime.now().strftime("%Y-%m-%d %H:%M")
                df_lain=st.session_state["data_pusat"][st.session_state["data_pusat"]['Kod_PPD']!=pilihan_ppd]
                st.session_state["data_pusat"]=pd.concat([df_lain,edited_df],ignore_index=True)
                simpan_ke_excel(); st.success("Update"); st.rerun()
    with tab_calon:
        st.subheader("🛠️ Calon & Petugas")
        df_edit=pd.DataFrame.from_dict(st.session_state["data_calon"],orient='index')
        edited_df2=st.data_editor(df_edit,use_container_width=True,num_rows="dynamic")
        if st.button("💾 SIMPAN DASHBOARD",type="primary",use_container_width=True):
            simpan_data_calon(edited_df2.to_dict(orient='index')); st.success("Update"); st.balloons(); st.rerun()
    if role=="Admin" and tab_mp is not None:
        with tab_mp:
            st.subheader("📚 MP - Admin")
            st.download_button("📥 Template MP",to_excel(pd.DataFrame(columns=COLUMNS_MP)),"template_mp.xlsx",use_container_width=True)
            up_mp=st.file_uploader("Upload MP",type=["xlsx"],key="up_mp")
            if up_mp:
                df_baru=pd.read_excel(up_mp,dtype=str)
                st.dataframe(df_baru.head(),use_container_width=True)
                if st.button("✅ Simpan MP",use_container_width=True):
                    st.session_state["data_mp"]=df_baru; simpan_ke_excel(); st.success("Simpan"); st.rerun()
    if role=="Admin" and tab_notis is not None:
        with tab_notis:
            data_n=load_notis()
            teks_baru=st.text_area("Teks Notis:",value=data_n.get("teks",""),height=120)
            up_img=st.file_uploader("Imej",type=["png","jpg","jpeg"],key="up_notis")
            if st.button("💾 Simpan Notis",type="primary",use_container_width=True):
                final_b64=data_n.get("image")
                if up_img: final_b64=base64.b64encode(up_img.getvalue()).decode()
                simpan_notis(teks_baru,final_b64); st.success("Simpan"); st.rerun()
    if role=="Admin" and tab_db is not None:
        with tab_db:
            st.subheader("💾 Urus File data_v1.1.xlsx")
            if os.path.exists(FILE_EXCEL):
                saiz=os.path.getsize(FILE_EXCEL)/1024
                tarikh=datetime.fromtimestamp(os.path.getmtime(FILE_EXCEL)).strftime("%Y-%m-%d %H:%M:%S")
                st.success(f"✅ WUJUD | {saiz:.1f} KB | {tarikh}")
                with open(FILE_EXCEL,"rb") as f:
                    st.download_button("📥 Download Backup",f.read(),FILE_EXCEL,use_container_width=True)
                st.write("---")
                st.error("⚠️ ZON BAHAYA - Password akashah")
                c1,c2=st.columns(2)
                with c1: confirm=st.checkbox("Saya faham & nak delete",key="confirm_del")
                with c2: pwd_del=st.text_input("Password Delete:",type="password",key="pwd_del",placeholder="••••••")
                boleh_delete=confirm and (pwd_del==PASSWORD_DELETE)
                if confirm and pwd_del!="" and pwd_del!=PASSWORD_DELETE: st.warning("❌ Salah!")
                elif boleh_delete: st.success("✅ Betul")
                if st.button("🗑️ DELETE FILE LAMA",type="primary",use_container_width=True,disabled=not boleh_delete):
                    os.remove(FILE_EXCEL)
                    st.session_state["data_pusat"]=pd.DataFrame(columns=COLUMNS_PUSAT)
                    st.session_state["data_mp"]=pd.DataFrame(columns=COLUMNS_MP)
                    st.success("Dipadam"); st.rerun()
            else: st.warning("❌ File TIADA")
            st.write("---")
            st.subheader("📤 Upload Baru")
            up_new=st.file_uploader("Pilih file baru",type=["xlsx"],key="up_new_db")
            if up_new:
                if st.button("✅ GANTI FILE V1.1",type="primary",use_container_width=True):
                    with open(FILE_EXCEL,"wb") as f: f.write(up_new.getbuffer())
                    st.session_state["data_pusat"]=load_data_pusat()
                    st.session_state["data_mp"]=load_data_mp()
                    st.success("Ganti"); st.balloons(); st.rerun()
            st.write("---")
            st.subheader("🔗 Buka Github - FIXED TAB BARU")
            pwd_github=st.text_input("Password Github:",type="password",key="pwd_github",placeholder="••••••")
            boleh_github=(pwd_github==PASSWORD_DELETE)
            if pwd_github!="" and not boleh_github: st.warning("❌ Salah!")
            elif boleh_github: st.success("✅ Betul - aktif")
            st.link_button("🌐 BUKA GITHUB SEKARANG",LINK_GITHUB_REPO,use_container_width=True,disabled=not boleh_github,type="primary")
            # --- DATA ASAL pecah pendek (elak line panjang) ---
DATA_ASAL = {
"Petaling Perdana": {"A-Sekolah Kerajaan":13106,"B-Sekolah Agensi":0,"C-Sekolah Bantuan Kerajaan":0,"D-Sekolah Swasta":571,"E-Calon Persendirian":974,"Penyelia Kawasan":30,"Ketua Pengawas":91,"Timbalan Ketua Pengawas":91,"Pengawas":1027,"Pengemas Bilik":91,"Sukarelawan":50},
"Petaling Utama": {"A-Sekolah Kerajaan":5209,"B-Sekolah Agensi":0,"C-Sekolah Bantuan Kerajaan":0,"D-Sekolah Swasta":317,"E-Calon Persendirian":491,"Penyelia Kawasan":22,"Ketua Pengawas":43,"Timbalan Ketua Pengawas":43,"Pengawas":494,"Pengemas Bilik":43,"Sukarelawan":50},
"Hulu Langat": {"A-Sekolah Kerajaan":12659,"B-Sekolah Agensi":4,"C-Sekolah Bantuan Kerajaan":32,"D-Sekolah Swasta":352,"E-Calon Persendirian":1150,"Penyelia Kawasan":32,"Ketua Pengawas":90,"Timbalan Ketua Pengawas":90,"Pengawas":1046,"Pengemas Bilik":90,"Sukarelawan":45},
"Gombak": {"A-Sekolah Kerajaan":9317,"B-Sekolah Agensi":0,"C-Sekolah Bantuan Kerajaan":0,"D-Sekolah Swasta":318,"E-Calon Persendirian":381,"Penyelia Kawasan":28,"Ketua Pengawas":61,"Timbalan Ketua Pengawas":61,"Pengawas":845,"Pengemas Bilik":61,"Sukarelawan":40},
"Klang": {"A-Sekolah Kerajaan":11742,"B-Sekolah Agensi":0,"C-Sekolah Bantuan Kerajaan":50,"D-Sekolah Swasta":941,"E-Calon Persendirian":791,"Penyelia Kawasan":30,"Ketua Pengawas":78,"Timbalan Ketua Pengawas":78,"Pengawas":863,"Pengemas Bilik":78,"Sukarelawan":48},
"Kuala Langat": {"A-Sekolah Kerajaan":4331,"B-Sekolah Agensi":0,"C-Sekolah Bantuan Kerajaan":44,"D-Sekolah Swasta":0,"E-Calon Persendirian":323,"Penyelia Kawasan":12,"Ketua Pengawas":32,"Timbalan Ketua Pengawas":32,"Pengawas":358,"Pengemas Bilik":32,"Sukarelawan":20},
"Kuala Selangor": {"A-Sekolah Kerajaan":4131,"B-Sekolah Agensi":5,"C-Sekolah Bantuan Kerajaan":0,"D-Sekolah Swasta":98,"E-Calon Persendirian":436,"Penyelia Kawasan":16,"Ketua Pengawas":31,"Timbalan Ketua Pengawas":31,"Pengawas":389,"Pengemas Bilik":31,"Sukarelawan":25},
"Hulu Selangor": {"A-Sekolah Kerajaan":3251,"B-Sekolah Agensi":104,"C-Sekolah Bantuan Kerajaan":0,"D-Sekolah Swasta":0,"E-Calon Persendirian":251,"Penyelia Kawasan":15,"Ketua Pengawas":26,"Timbalan Ketua Pengawas":26,"Pengawas":240,"Pengemas Bilik":26,"Sukarelawan":18},
"Sabak Bernam": {"A-Sekolah Kerajaan":1990,"B-Sekolah Agensi":158,"C-Sekolah Bantuan Kerajaan":58,"D-Sekolah Swasta":16,"E-Calon Persendirian":85,"Penyelia Kawasan":12,"Ketua Pengawas":24,"Timbalan Ketua Pengawas":24,"Pengawas":197,"Pengemas Bilik":24,"Sukarelawan":15},
"Sepang": {"A-Sekolah Kerajaan":3477,"B-Sekolah Agensi":0,"C-Sekolah Bantuan Kerajaan":48,"D-Sekolah Swasta":110,"E-Calon Persendirian":382,"Penyelia Kawasan":22,"Ketua Pengawas":28,"Timbalan Ketua Pengawas":28,"Pengawas":265,"Pengemas Bilik":28,"Sukarelawan":30}
}

def load_data_calon():
    if os.path.exists(FILE_CALON_JSON):
        try:
            with open(FILE_CALON_JSON,"r") as f: return json.load(f)
        except: return DATA_ASAL
    else: return DATA_ASAL
def simpan_data_calon(data):
    with open(FILE_CALON_JSON,"w") as f: json.dump(data,f,indent=2)
    st.session_state["data_calon"]=data
def load_data_pusat():
    if os.path.exists(FILE_EXCEL):
        try: return pd.read_excel(FILE_EXCEL,sheet_name=SHEET_PUSAT,engine='openpyxl',dtype=str)
        except: return pd.DataFrame(columns=COLUMNS_PUSAT)
    else: return pd.DataFrame(columns=COLUMNS_PUSAT)
def load_data_mp():
    if os.path.exists(FILE_EXCEL):
        try: return pd.read_excel(FILE_EXCEL,sheet_name=SHEET_MP,engine='openpyxl',dtype=str)
        except: return pd.DataFrame(columns=COLUMNS_MP)
    else: return pd.DataFrame(columns=COLUMNS_MP)
def to_excel(df):
    output=BytesIO()
    with pd.ExcelWriter(output,engine='openpyxl') as writer: df.to_excel(writer,index=False)
    return output.getvalue()
def simpan_ke_excel():
    with pd.ExcelWriter(FILE_EXCEL,engine='openpyxl',mode='w') as writer:
        st.session_state["data_pusat"].to_excel(writer,sheet_name=SHEET_PUSAT,index=False)
        st.session_state["data_mp"].to_excel(writer,sheet_name=SHEET_MP,index=False)
def simpan_data_pusat(kod_ppd,no_pusat,nama_pusat,bil_calon,nama_kebal,dikemaskini_oleh):
    df=st.session_state["data_pusat"]
    df=df[df['No_Pusat']!=no_pusat]
    data_baru=pd.DataFrame([{'Kod_PPD':kod_ppd,'No_Pusat':no_pusat,'Nama_Pusat':nama_pusat,'Bil_Calon_Pusat':bil_calon,'Nama_Bilik_Kebal':nama_kebal,'Dikemaskini_Oleh':dikemaskini_oleh,'Tarikh_Kemaskini':datetime.now().strftime("%Y-%m-%d %H:%M")}])
    st.session_state["data_pusat"]=pd.concat([df,data_baru],ignore_index=True)
    simpan_ke_excel()

# --- SETUP SESSION ---
if "data_calon" not in st.session_state: st.session_state["data_calon"]=load_data_calon()
if "data_pusat" not in st.session_state: st.session_state["data_pusat"]=load_data_pusat()
if "data_mp" not in st.session_state: st.session_state["data_mp"]=load_data_mp()
if "editor_login" not in st.session_state: st.session_state["editor_login"]=False
if "show_editor" not in st.session_state: st.session_state["show_editor"]=False
if "menu" not in st.session_state: st.session_state["menu"]="Dashboard"

def login_editor():
    with st.form("login_form"):
        u=st.text_input("Nama Pengguna",key="user_login")
        p=st.text_input("Kata Laluan",type="password",key="pass_login")
        if st.form_submit_button("Log Masuk",use_container_width=True,type="primary"):
            uname=u.lower().strip()
            if uname in USERS and USERS[uname]["password"]==p:
                st.session_state["editor_login"]=True
                st.session_state["username"]=uname
                st.session_state["role"]=USERS[uname]["role"]
                if USERS[uname]["role"]=="PPD":
                    st.session_state["daerah_ppd"]=USERS[uname]["daerah"]
                    st.session_state["kod_ppd"]=KOD_PPD[USERS[uname]["daerah"]]
                st.success("Login ok"); st.rerun()
            else: st.error("Salah!")

# --- PAGE SELENGGARA (5 TAB + GITHUB FIX) ---
def page_selenggara_pusat():
    st.header("⚙️ Selenggara Data")
    if not st.session_state.get("editor_login",False):
        st.warning("Login dulu"); return
    role=st.session_state.get("role","")
    if role=="Admin":
        tab_pusat,tab_mp,tab_calon,tab_notis,tab_db=st.tabs(["🏫 Pusat","📚 MP","👥 Calon","📢 Notis","💾 Urus File + Github"])
    else:
        tab_pusat,tab_calon=st.tabs(["🏫 Pusat","👥 Calon"])
        tab_mp=None; tab_notis=None; tab_db=None
    with tab_pusat:
        pilihan_ppd=st.selectbox("Pilih PPD",list(KOD_PPD.values())) if role=="Admin" else st.session_state["kod_ppd"]
        with st.form("form_pusat"):
            c1,c2=st.columns(2)
            with c1:
                no_pusat=st.text_input("No Pusat *")
                nama_pusat=st.text_input("Nama Pusat *")
            with c2:
                bil_calon=st.number_input("Bil Calon",min_value=0,step=1)
                nama_kebal=st.text_input("Bilik Kebal")
            if st.form_submit_button("💾 Simpan",type="primary",use_container_width=True):
                if no_pusat and nama_pusat:
                    simpan_data_pusat(pilihan_ppd,no_pusat,nama_pusat,bil_calon,nama_kebal,st.session_state["username"])
                    st.success("Disimpan"); st.rerun()
        df_tunjuk=st.session_state["data_pusat"][st.session_state["data_pusat"]['Kod_PPD']==pilihan_ppd]
        edited_df=st.data_editor(df_tunjuk,use_container_width=True,num_rows="dynamic",key=f"ed_{pilihan_ppd}")
        if st.button("💾 SIMPAN EDIT",type="primary",use_container_width=True):
            if not edited_df.empty:
                edited_df['Dikemaskini_Oleh']=st.session_state["username"]
                edited_df['Tarikh_Kemaskini']=datetime.now().strftime("%Y-%m-%d %H:%M")
                df_lain=st.session_state["data_pusat"][st.session_state["data_pusat"]['Kod_PPD']!=pilihan_ppd]
                st.session_state["data_pusat"]=pd.concat([df_lain,edited_df],ignore_index=True)
                simpan_ke_excel(); st.success("Update"); st.rerun()
    with tab_calon:
        df_edit=pd.DataFrame.from_dict(st.session_state["data_calon"],orient='index')
        edited_df2=st.data_editor(df_edit,use_container_width=True,num_rows="dynamic")
        if st.button("💾 SIMPAN DASHBOARD",type="primary",use_container_width=True):
            simpan_data_calon(edited_df2.to_dict(orient='index')); st.success("Update"); st.balloons(); st.rerun()
    if role=="Admin" and tab_mp is not None:
        with tab_mp:
            st.download_button("📥 Template MP",to_excel(pd.DataFrame(columns=COLUMNS_MP)),"template_mp.xlsx",use_container_width=True)
            up_mp=st.file_uploader("Upload MP",type=["xlsx"],key="up_mp")
            if up_mp:
                df_baru=pd.read_excel(up_mp,dtype=str)
                st.dataframe(df_baru.head(),use_container_width=True)
                if st.button("✅ Simpan MP",use_container_width=True):
                    st.session_state["data_mp"]=df_baru; simpan_ke_excel(); st.success("Simpan"); st.rerun()
    if role=="Admin" and tab_notis is not None:
        with tab_notis:
            from pathlib import Path
            def load_notis2():
                if os.path.exists(FILE_NOTIS):
                    try:
                        with open(FILE_NOTIS,"r",encoding="utf-8") as f:
                            d=json.load(f); return d.get("teks",DEFAULT_NOTIS)
                    except: return DEFAULT_NOTIS
                return DEFAULT_NOTIS
            teks=st.text_area("Teks Notis:",value=load_notis2(),height=120)
            if st.button("💾 Simpan Notis",type="primary",use_container_width=True):
                with open(FILE_NOTIS,"w",encoding="utf-8") as f:
                    json.dump({"teks":teks},f,ensure_ascii=False,indent=2)
                st.success("Simpan"); st.rerun()
    if role=="Admin" and tab_db is not None:
        with tab_db:
            st.subheader("💾 Urus File data_v1.1.xlsx + Github FIXED")
            if os.path.exists(FILE_EXCEL):
                saiz=os.path.getsize(FILE_EXCEL)/1024
                st.success(f"✅ WUJUD | {saiz:.1f} KB")
                with open(FILE_EXCEL,"rb") as f:
                    st.download_button("📥 Download Backup",f.read(),FILE_EXCEL,use_container_width=True)
                st.write("---")
                c1,c2=st.columns(2)
                with c1: confirm=st.checkbox("Saya faham & nak delete",key="confirm_del")
                with c2: pwd_del=st.text_input("Password Delete:",type="password",key="pwd_del",placeholder="••••••")
                boleh_delete=confirm and (pwd_del==PASSWORD_DELETE)
                if st.button("🗑️ DELETE FILE LAMA",type="primary",use_container_width=True,disabled=not boleh_delete):
                    os.remove(FILE_EXCEL); st.success("Dipadam"); st.rerun()
            else: st.warning("❌ File TIADA")
            st.write("---")
            up_new=st.file_uploader("Upload file baru",type=["xlsx"],key="up_new_db")
            if up_new:
                if st.button("✅ GANTI FILE V1.1",type="primary",use_container_width=True):
                    with open(FILE_EXCEL,"wb") as f: f.write(up_new.getbuffer())
                    st.session_state["data_pusat"]=load_data_pusat()
                    st.session_state["data_mp"]=load_data_mp()
                    st.success("Ganti"); st.balloons(); st.rerun()
            st.write("---")
            st.subheader("🔗 Buka Github - Password Protected")
            pwd_github=st.text_input("Password Github:",type="password",key="pwd_github",placeholder="••••••")
            boleh_github=(pwd_github==PASSWORD_DELETE)
            if boleh_github: st.success("✅ Password betul")
            # FIXED - TAB BARU, TAK REFUSED
            st.link_button("🌐 BUKA GITHUB SEKARANG - TAB BARU",LINK_GITHUB_REPO,use_container_width=True,disabled=not boleh_github,type="primary")

def page_dashboard():
    data=st.session_state["data_calon"]
    daerah=st.session_state.get("filter_daerah","Semua Daerah")
    cA,cB,cC=st.columns(3)
    total_calon=sum(sum(data[d][k] for k in JENIS_CALON[1:]) for d in data)
    total_petugas=sum(sum(data[d][k] for k in JENIS_PETUGAS[1:]) for d in data)
    total_pusat=sum(data[d]["Ketua Pengawas"] for d in data)
    with cA: st.metric("Calon",f"{total_calon:,}")
    with cB: st.metric("Petugas",f"{total_petugas:,}")
    with cC: st.metric("Pusat",f"{total_pusat:,}")
    df_calon=pd.DataFrame([{k:v[k] for k in JENIS_CALON[1:]} for v in data.values()],index=data.keys())
    st.dataframe(df_calon,use_container_width=True)
    fig1,ax1=plt.subplots(figsize=(11,5))
    df_calon.plot(kind='bar',ax=ax1); st.pyplot(fig1)

# --- HEADER ---
if os.path.exists("logo.png"):
    with open("logo.png","rb") as f:
        logo_b64=base64.b64encode(f.read()).decode()
        logo_html=f'<img src="data:image/png;base64,{logo_b64}" width="90">'
else: logo_html="🏛️"
st.markdown(f'<div style="background:linear-gradient(90deg,#004D40 0%,#00695C 100%);border:2px solid #FFD700;border-radius:15px;padding:12px;display:flex;align-items:center;"><div style="margin-right:15px;">{logo_html}</div><div><div style="color:#FFD700;font-weight:bold;font-size:22px;">JABATAN PENDIDIKAN SELANGOR</div><div style="color:white;">SEKTOR PENTAKSIRAN DAN PEPERIKSAAN - SPM</div></div></div>',unsafe_allow_html=True)

col_sidebar,col_main=st.columns([1,4])
with col_sidebar:
    st.markdown("### Menu")
    if st.button("📊 Dashboard",use_container_width=True): st.session_state["menu"]="Dashboard"; st.rerun()
    if st.button("📋 Senarai Pusat",use_container_width=True): st.session_state["menu"]="SenaraiPusat"; st.rerun()
    if st.button("📚 Cari MP",use_container_width=True): st.session_state["menu"]="CariMP"; st.rerun()
    if st.button("🛠️ Selenggara",use_container_width=True): st.session_state["show_editor"]=not st.session_state["show_editor"]
    if st.session_state.get("editor_login",False):
        if st.button("🛠️ Buka Selenggara",type="primary",use_container_width=True): st.session_state["menu"]="Selenggara"; st.rerun()
    if st.session_state["show_editor"]:
        if not st.session_state.get("editor_login",False): login_editor()
        else:
            st.success(f"Login: {st.session_state['username']}")
            if st.button("Log Keluar",use_container_width=True): st.session_state["editor_login"]=False; st.session_state["show_editor"]=False; st.rerun()

with col_main:
    if st.session_state["menu"]=="Dashboard": page_dashboard()
    elif st.session_state["menu"]=="Selenggara": page_selenggara_pusat()
    elif st.session_state["menu"]=="SenaraiPusat":
        st.header("📋 Senarai Pusat")
        st.dataframe(st.session_state["data_pusat"],use_container_width=True)
    elif st.session_state["menu"]=="CariMP":
        st.header("📚 Carian MP")
        st.dataframe(st.session_state["data_mp"],use_container_width=True)
