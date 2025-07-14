# ui.py

import streamlit as st
from views import urlaub_view, schichtplan_view, kalender_view, dashboard_view

def render_navigation():
    st.sidebar.title("Navigation")
    choice = st.sidebar.radio("Seite wählen", ["Dashboard", "Urlaubsplanung", "Schichtplan", "Kalender"])

    if choice == "Dashboard":
        dashboard_view()
    elif choice == "Urlaubsplanung":
        urlaub_view()
    elif choice == "Schichtplan":
        schichtplan_view()
    elif choice == "Kalender":
        kalender_view()
