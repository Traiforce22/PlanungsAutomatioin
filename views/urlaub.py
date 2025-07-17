# views/urlaub.py

import streamlit as st
from sqlalchemy.orm import Session
from db.models import Mitarbeiter, Urlaub
from db.session import SessionLocal
from datetime import date

def urlaub_view():
    st.header("🗓️ Urlaubsplanung")

    db: Session = SessionLocal()

    # Mitarbeitende abrufen
    mitarbeiter_liste = db.query(Mitarbeiter).all()
    if not mitarbeiter_liste:
        st.warning("Bitte zuerst Mitarbeitende anlegen.")
        return

    name_map = {m.name: m.id for m in mitarbeiter_liste}

    with st.form("urlaub_formular"):
        name = st.selectbox("Mitarbeiter", list(name_map.keys()))
        von = st.date_input("Von", date.today())
        bis = st.date_input("Bis", date.today())
        status = st.selectbox("Status", ["offen", "bestätigt", "abgelehnt"])
        speichern = st.form_submit_button("Speichern")

        if speichern:
            neuer_urlaub = Urlaub(
                mitarbeiter_id=name_map[name],
                von=von,
                bis=bis,
                status=status
            )
            db.add(neuer_urlaub)
            db.commit()
            st.success("Urlaub gespeichert.")

    # Bestehende Urlaube anzeigen
    urlaube = db.query(Urlaub).all()
    if urlaube:
        st.subheader("Alle Urlaube")
        for eintrag in urlaube:
            st.write(f"• {eintrag.mitarbeiter.name} | {eintrag.von} bis {eintrag.bis} | Status: {eintrag.status}")
    else:
        st.info("Keine Urlaube erfasst.")

    db.close()
