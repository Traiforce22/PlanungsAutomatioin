# views/dashboard.py

import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime, timedelta
from db.session import SessionLocal
from db.models import SonderOeffnungszeiten # ggf. auch Urlaub, Schicht etc.

def dashboard_view():
    st.title("📅 Dashboard – Kalenderübersicht")

    # Auswahl, was im Kalender angezeigt werden soll
    auswahl = st.multiselect(
        "Anzeigen:",
        ["Sonderöffnungszeiten", "Schichten", "Urlaube", "Events"],
        default=["Sonderöffnungszeiten"]
    )

    db = SessionLocal()
    einträge = []

    if "Sonderöffnungszeiten" in auswahl:
        sonder = db.query(SonderOeffnungszeiten).all()
        for eintrag in sonder:
            einträge.append({
                "title": f"Sonderöffnung: {eintrag.beschreibung or ''}",
                "start": eintrag.datum.strftime("%Y-%m-%d") + "T" + eintrag.von.strftime("%H:%M:%S"),
                "end": eintrag.datum.strftime("%Y-%m-%d") + "T" + eintrag.bis.strftime("%H:%M:%S"),
                "color": "#00C853",  # grün
            })

    # Weitere Einträge wie Schichten oder Urlaube:
    # if "Schichten" in auswahl:
    #     ...

    calendar_options = {
        "initialView": "dayGridMonth",
        "slotMinTime": "09:00:00",
        "slotMaxTime": "23:00:00",
        "height": 900,
        "locale": "de",
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,timeGridDay"
        },
    }

    calendar(events=einträge, options=calendar_options)
    db.close()
