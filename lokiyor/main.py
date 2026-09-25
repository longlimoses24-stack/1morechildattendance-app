import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- Configuration & Passcode ---
STAFF_PASSCODE = "longoli2004"  # Set your staff passcode here
LOG_FILE = "1morechild_attendance_log.csv"

# Preset editable lists
DEFAULT_STAFF = ["Lounga Benson", "Losire Mark", "Mukiibi Bosco", "Chero Sylvia", "Yeno Annet",
                 "Aila Lydia", "Emong Emmanuel", "Muya James", "Martha", "Dorothy",
                 "Logiel Evelyn"]

DEFAULT_CHILDREN = ["Otyang James", "Lokwii Michael", "Longole Moses", "Sagal Christine", "Ajalun John",
                    "Ethin Rose", "Lojale Vicky", "Maruk Michael", "Sagal Paul", "Lowal Paul",
                    "Lochikiri Emmanuel", "Lokure John Bosco", "Angolere Samuel", "Abol Mark", "Dengel David",
                    "Loruk Francis", "Lopido Paul", "Lojut Jesse", "Kodet Godfrey", "Lopiri John Bosco",
                    "Koluo Joshua", "Aguma Mark", "Namuke Betty", "Lokol Hellen",
                    "Anyakun Abraham", "Nachap Veronica", "Ichumar Emmanuel", "Loukai Jeremaih", "Kodet Mary",
                    "Longora Angellina", "Longoli Hannah", "Nadiye Mary", "Angella Mary", "Munyes Oliver",
                    "Nakiru Angelina", "Keem Winnie", "Ngorok Peter", "Lochoro Patrick",
                    "Namuria Rose", "Lotukei Mary", "Longoli Mary", "Lokutai Erinah", "Lokwang Matiya",
                    "Hawuwa Caroline", "Itawoi Johnathan", "Lochuwa Michael", "Akol Mary", "Wani James",
                    "Lomilo Caroline", "Anyakun Daniel", "Kodet Pascal", "Lokol Emmanuel", "Ojok Paul",
                    "Sagal Emmanuel", "Longole Esther", "Lopur William", "Lotonia Moses",
                    "Kalembe Desire", "Abura Paul", "Akello Rachael", "Lomokol Emmanuel", "Apalia Emmanuel",
                    "Koriang Paul", "Munyango Mathew", "Loriko Moses", "Lora Bosco", "Kedia John",
                    "Longes Moses", "Lokuta Robert", "Lokiyor Francis", "Agan Joshua", "Achen Lucy",
                    "Iriama Mercy", "Lomilo Emmanuel", "Dikiri Jane", "Aleper Charles", "Lochugai Paul",
                    "Mutebi Meddy", "Achia Samuel", "Loogos Emmanuel", "Imalany Joseph", "Loduk Michael",
                    "Modo Peace", "Sagal John"]

st.set_page_config(page_title="1moreChild Attendance", page_icon="📋")
st.title("📋 1moreChild Attendance System")

# --- Authentication Logic ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

with st.sidebar:
    st.header("🔐 Staff Authentication")
    if not st.session_state.authenticated:
        passcode_input = st.text_input("Enter Staff Passcode:", type="password")
        if st.button("Unlock Admin Access"):
            if passcode_input == STAFF_PASSCODE:
                st.session_state.authenticated = True
                st.success("Access Granted!")
                st.rerun()
            else:
                st.error("Incorrect Passcode")
    else:
        st.success("🔓 Admin Mode Active")
        if st.button("Lock App"):
            st.session_state.authenticated = False
            st.rerun()


def save_attendance(category, records):
    date_str = datetime.now().strftime("%Y-%m-%d")
    time_str = datetime.now().strftime("%H:%M:%S")

    rows = []
    for name, status in records.items():
        rows.append({
            "Date": date_str,
            "Time": time_str,
            "Category": category,
            "Name": name,
            "Status": status
        })

    df_new = pd.DataFrame(rows)
    if os.path.exists(LOG_FILE):
        df_new.to_csv(LOG_FILE, mode='a', header=False, index=False)
    else:
        df_new.to_csv(LOG_FILE, index=False)
    st.success(f"{category} attendance saved successfully!")


# --- Dynamic Tabs based on Authentication ---
if st.session_state.authenticated:
    tab1, tab2, tab3 = st.tabs(["Staff Attendance", "Children Attendance", "📊 View Log (Admin)"])
else:
    tab1, tab2 = st.tabs(["Staff Attendance", "Children Attendance"])
    tab3 = None

# --- Staff Tab ---
with tab1:
    st.header("Staff Attendance")
    staff_status = {}
    for name in DEFAULT_STAFF:
        staff_status[name] = st.radio(f"{name}", ["Present", "Absent", "Late"], key=f"staff_{name}", horizontal=True)

    if st.button("Submit Staff Attendance"):
        save_attendance("Staff", staff_status)

# --- Children Tab ---
with tab2:
    st.header("Children Attendance")
    children_status = {}
    for name in DEFAULT_CHILDREN:
        children_status[name] = st.radio(f"{name}", ["Present", "Absent", "Late"], key=f"child_{name}", horizontal=True)

    if st.button("Submit Children Attendance"):
        save_attendance("Children", children_status)

# --- View Log Tab (Protected) ---
if tab3:
    with tab3:
        st.header("Attendance Records")
        if os.path.exists(LOG_FILE):
            df = pd.read_csv(LOG_FILE)
            st.dataframe(df, use_container_width=True)
            st.download_button("Download CSV Log", df.to_csv(index=False), "attendance_log.csv", "text/csv")
        else:
            st.info("No records recorded yet.")
