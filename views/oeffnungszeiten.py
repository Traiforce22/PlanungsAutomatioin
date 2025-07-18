# views/oeffnungszeiten.py

import streamlit as st
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from db.models import Oeffnungszeiten, SonderOeffnungszeiten
from db.session import SessionLocal
from datetime import time, date

def oeffnungszeiten_view():
    st.header("🕛 Öffnungszeiten")

    weekdays = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    db = SessionLocal()

    st.subheader("Regelmäßige Öffnungszeiten")
    zeiten = {eintrag.wochentag: eintrag for eintrag in db.query(Oeffnungszeiten).all()}

    for tag in weekdays:
        with st.expander(tag):
            eintrag = zeiten.get(tag)
            von = st.time_input(f"{tag} von", eintrag.von if eintrag else time(9, 0), key=f"von_{tag}")
            bis = st.time_input(f"{tag} bis", eintrag.bis if eintrag else time(17, 0), key=f"bis_{tag}")

            if st.button(f"Speichern {tag}", key=f"save_{tag}"):
                try:
                    if eintrag:
                        eintrag.von = von
                        eintrag.bis = bis
                    else:
                        db.add(Oeffnungszeiten(wochentag=tag, von=von, bis=bis))
                    db.commit()
                    st.success(f"Öffnungszeiten für {tag} gespeichert")
                except SQLAlchemyError as e:
                    db.rollback()
                    st.error("Fehler beim Speichern")
                    st.exception(e)

    st.divider()
    st.subheader("Sonderöffnungszeiten")

    with st.form("sonder_form"):
        datum = st.date_input("Datum")
        von = st.time_input("Von", time(9, 0))
        bis = st.time_input("Bis", time(17, 0))
        beschreibung = st.text_input("Beschreibung (Name der Sonderöffnung)")
        speichern = st.form_submit_button("Hinzufügen")

        if speichern:
            try:
                neuer = SonderOeffnungszeiten(datum=datum, von=von, bis=bis, beschreibung=beschreibung)
                db.add(neuer)
                db.commit()
                st.success("Sondereintrag gespeichert")
            except SQLAlchemyError as e:
                db.rollback()
                st.error("Fehler beim Speichern")
                st.exception(e)

    sonder_liste = db.query(SonderOeffnungszeiten).order_by(SonderOeffnungszeiten.datum).all()
    if sonder_liste:
        st.markdown("### Übersicht der Sonderöffnungszeiten")
        for eintrag in sonder_liste:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"{eintrag.datum.strftime('%d.%m.%Y')}: {eintrag.von.strftime('%H:%M')} – {eintrag.bis.strftime('%H:%M')} {eintrag.beschreibung or ''}")
            with col2:
                if st.button("Löschen", key=f"del_sonder_{eintrag.id}"):
                    try:
                        db.delete(eintrag)
                        db.commit()
                        st.success("Eintrag gelöscht")
                        st.rerun()
                    except SQLAlchemyError as e:
                        db.rollback()
                        st.error("Fehler beim Löschen")
                        st.exception(e)

    db.close()
