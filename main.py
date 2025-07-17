# main.py

from db.session import engine
from db.models import Base
import streamlit as st
from views.urlaub import urlaub_view
from views.mitarbeiter import mitarbeiter_view
from views.dashboard import dashboard_view


# Create tables if not yet present
Base.metadata.create_all(bind=engine)

# App-Konfiguration

st.set_page_config(page_title="Schicht- & Urlaubsplaner", layout="wide")
page = st.sidebar.radio("Gehe zu", ["Dashboard", "Ulraub", "Mitarbeiter-Management"])

if page == "Mitarbeiter-Management":
    mitarbeiter_view()
elif page == "Ulraub":
    urlaub_view()
else:
    dashboard_view()
