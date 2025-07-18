# main.py

from db.session import engine
from db.models import Base
import streamlit as st
from views.urlaub import urlaub_view
from views.mitarbeiter import mitarbeiter_view
from views.dashboard import dashboard_view
from views.oeffnungszeiten import oeffnungszeiten_view


# Create tables if not yet present
Base.metadata.create_all(bind=engine)

# App-Konfiguration

st.set_page_config(page_title="Schicht- & Urlaubsplaner", layout="wide")
pages = {
    "Dashboard": dashboard_view,
    "Urlaub": urlaub_view,
    "Mitarbeiter": mitarbeiter_view,
    "Öffnungszeiten": oeffnungszeiten_view,  # optional, only if implemented
}

selected_page = st.sidebar.radio("📂 Navigation", list(pages.keys()))
pages[selected_page]() 
