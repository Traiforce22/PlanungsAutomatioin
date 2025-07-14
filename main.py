# main.py

import streamlit as st
from db import init_db
from ui import render_navigation

# App-Konfiguration
st.set_page_config(page_title="Schicht- & Urlaubsplaner", layout="wide")

# Datenbank initialisieren
init_db()

# Navigationsbereich / Seiteninhalt laden
render_navigation()
