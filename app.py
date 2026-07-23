import streamlit as st
import pandas as pd
from datetime import datetime

# --- SEITEN-KONFIGURATION ---
st.set_page_config(
    page_title="Akeno AG | Jobcoaching Management",
    page_icon="💼",
    layout="wide"
)

# --- INDIVIDUELLES DESIGN (Akeno AG Branding) ---
st.markdown("""
    <style>
    .main-header {
        font-size: 28px;
        color: #1E3A8A;
        font-weight: bold;
        border-bottom: 2px solid #1E3A8A;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    .stButton>button {
        background-color: #1E3A8A;
        color: white;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALISIERUNG (Daten-Zwischenspeicher) ---
if "klienten" not in st.session_state:
    st.session_state.klienten = [
        {"ID": 101, "Name": "Max Muster", "Status": "In Bewerbungsphase", "Coach": "Akeno Team", "Eintritt": "2026-01-15"},
        {"ID": 102, "Name": "Anna Beispiel", "Status": "Erstgespräch", "Coach": "Akeno Team", "Eintritt": "2026-02-01"}
    ]

if "bewerbungen" not in st.session_state:
    st.session_state.bewerbungen = [
        {"Klient": "Max Muster", "Firma": "Tech AG", "Stelle": "Projektleiter", "Status": "Eingereicht", "Datum": "2026-02-10"}
    ]

# --- NAVIGATION SIDEBAR ---
st.sidebar.image("https://www.akenoag.ch/favicon.ico", width=50) # Platzhalter
st.sidebar.title("Akeno AG Coaching")
menu = st.sidebar.radio("Navigation", ["Dashboard & Klienten", "Bewerbungstracker", "IN-Qualis Checkliste"])

# --- SEITE 1: DASHBOARD & KLIENTEN ---
if menu == "Dashboard & Klienten":
    st.markdown('<div class="main-header">👥 Klientenverwaltung</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Aktive Klienten")
        df_klienten = pd.DataFrame(st.session_state.klienten)
        st.dataframe(df_klienten, use_container_width=True)
        
    with col2:
        st.subheader("Neuen Klienten erfassen")
        with st.form("neuer_klient_form"):
            name = st.text_input("Name, Vorname")
            status = st.selectbox("Status", ["Erstgespräch", "In Begleitung", "In Bewerbungsphase", "Erfolgreich Vermittelt", "Abgeschlossen"])
            coach = st.text_input("Zuständiger Coach", value="Akeno Coach")
            submitted = st.form_submit_button("Klient Anlegen")
            
            if submitted and name:
                neue_id = len(st.session_state.klienten) + 101
                neuer_eintrag = {
                    "ID": neue_id,
                    "Name": name,
                    "Status": status,
                    "Coach": coach,
                    "Eintritt": datetime.now().strftime("%Y-%m-%d")
                }
                st.session_state.klienten.append(neuer_eintrag)
                st.success(f"Klient {name} wurde erfolgreich erfasst!")
                st.rerun()

# --- SEITE 2: BEWERBUNGSTRACKER ---
elif menu == "Bewerbungstracker":
    st.markdown('<div class="main-header">🎯 Bewerbungstracker</div>', unsafe_allow_html=True)
    
    klienten_liste = [k["Name"] for k in st.session_state.klienten]
    
    st.subheader("Bewerbung hinzufügen")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        selected_klient = st.selectbox("Klient", klienten_liste)
    with c2:
        firma = st.text_input("Arbeitgeber / Firma")
    with c3:
        stelle = st.text_input("Stelle / Funktion")
    with c4:
        bew_status = st.selectbox("Status", ["Pendent", "Eingereicht", "Einladung Gespräch", "Absage", "Zusage"])
        
    if st.button("Bewerbung Speichern"):
        if firma and stelle:
            st.session_state.bewerbungen.append({
                "Klient": selected_klient,
                "Firma": firma,
                "Stelle": stelle,
                "Status": bew_status,
                "Datum": datetime.now().strftime("%Y-%m-%d")
            })
            st.success("Bewerbung protokolliert!")
            st.rerun()

    st.markdown("---")
    st.subheader("Übersicht aller Bewerbungen")
    st.dataframe(pd.DataFrame(st.session_state.bewerbungen), use_container_width=True)

# --- SEITE 3: IN-QUALIS AUDIT CHECKLISTE ---
elif menu == "IN-Qualis Checkliste":
    st.markdown('<div class="main-header">📋 IN-Qualis 2024 Audit-Vorbereitung</div>', unsafe_allow_html=True)
    st.info("Übersicht der erforderlichen Dokumente für das Stufe-1-Audit gemäss IN-Qualis Norm.")
    
    checkliste = [
        "Organigramm & Funktionendiagramm",
        "Prozesslandkarte & Prozessbeschriebe",
        "Strategie und strategische Ziele",
        "Qualitätspolitik & Risikomanagement",
        "Konzept zum organisationsinternen Fallmanagement (Modul B)",
        "Konzepte der einzelnen Angebote (Module C)",
        "Evaluationsberichte & Managementreview"
    ]
    
    for item in checkliste:
        st.checkbox(item, key=item)
