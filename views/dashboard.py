import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime, timedelta

def dashboard_view():
    st.title("📅 Dashboard – Kalenderübersicht")

    # Sample events (could be fetched from DB later)
    events = [
        {
            "title": "Max Urlaub",
            "start": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "end": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
            "color": "#FF5733",
        },
        {
            "title": "Frühschicht – Anna",
            "start": datetime.now().strftime("%Y-%m-%d"),
            "color": "#33B5FF",
        },
    ]

    calendar_options = {
        "initialView": "dayGridMonth",
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,timeGridDay"
        },
        "locale": "de",
        "events": events
    }

    calendar(events=events, options=calendar_options)
