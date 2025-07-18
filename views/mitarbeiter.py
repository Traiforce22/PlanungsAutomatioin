# views/mitarbeiter.py

import streamlit as st
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from db.models import Mitarbeiter, WoechentlicheSchicht
from db.session import SessionLocal
from datetime import time

def mitarbeiter_view():
    st.header("Übersicht Mitarbeitende")

    st.subheader("📋 Mitarbeitendenübersicht mit Wochenschichten")

    weekdays = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]

    db = SessionLocal()
    mitarbeiter_liste = db.query(Mitarbeiter).all()

    for mitarbeiter in mitarbeiter_liste:
        st.markdown(f"### 🧑 {mitarbeiter.name} {mitarbeiter.nachname}")

        # Schichten laden
        schichten = {
            schicht.wochentag: schicht
            for schicht in mitarbeiter.woechentlicheschichten
        }

        is_editing = st.checkbox(f"Bearbeiten ({mitarbeiter.name})", key=f"edit_{mitarbeiter.id}")
        cols = st.columns([1] * len(weekdays))

        for i, wtag in enumerate(weekdays):
            with cols[i]:
                existing = schichten.get(wtag)
                if is_editing:
                    von = st.time_input(
                        f"{wtag[:2]} von",
                        existing.von if existing else time(8, 0),
                        key=f"von_{mitarbeiter.id}_{wtag}"
                    )
                    bis = st.time_input(
                        f"{wtag[:2]} bis",
                        existing.bis if existing else time(16, 0),
                        key=f"bis_{mitarbeiter.id}_{wtag}"
                    )

                    if st.button(f"Speichern {wtag}", key=f"save_{mitarbeiter.id}_{wtag}"):
                        try:
                            if existing:
                                existing.von = von
                                existing.bis = bis
                            else:
                                neue_schicht = WoechentlicheSchicht(
                                    mitarbeiter_id=mitarbeiter.id,
                                    wochentag=wtag,
                                    von=von,
                                    bis=bis
                                )
                                db.add(neue_schicht)
                            db.commit()
                            st.success(f"{wtag}-Schicht gespeichert")
                        except SQLAlchemyError as e:
                            db.rollback()
                            st.error("Fehler beim Speichern")
                            st.exception(e)
                    if existing and st.button(f"Löschen {wtag}", key=f"del_{mitarbeiter.id}_{wtag}"):
                        try:
                            db.delete(existing)
                            db.commit()
                            st.success(f"{wtag}-Schicht gelöscht")
                        except SQLAlchemyError as e:
                            db.rollback()
                            st.error("Fehler beim Löschen")
                            st.exception(e)
                else:
                    if existing:
                        st.markdown(
                            f"<div style='background-color:{mitarbeiter.farbe}; padding:6px; border-radius:5px; text-align:center;'>"
                            f"{existing.von.strftime('%H:%M')} – {existing.bis.strftime('%H:%M')}"
                            f"</div>",
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown("<span style='color:gray'>–</span>", unsafe_allow_html=True)
        with cols[-1]:
            if st.button("🗑️ Mitarbeiter löschen", key=f"show_del_{mitarbeiter.id}"):
                st.session_state[f"confirm_delete_{mitarbeiter.id}"] = True

        if st.session_state.get(f"confirm_delete_{mitarbeiter.id}", False):
            st.warning(f"❗ Möchtest du {mitarbeiter.name} {mitarbeiter.nachname} wirklich löschen?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Ja, löschen", key=f"confirm_del_{mitarbeiter.id}"):
                    try:
                        db.delete(mitarbeiter)
                        db.commit()
                        st.success(f"{mitarbeiter.name} {mitarbeiter.nachname} wurde gelöscht")
                        st.session_state.pop(f"confirm_delete_{mitarbeiter.id}", None)
                        st.rerun()
                    except SQLAlchemyError as e:
                        db.rollback()
                        st.error("Fehler beim Löschen")
                        st.exception(e)
            with col2:
                if st.button("Abbrechen", key=f"cancel_del_{mitarbeiter.id}"):
                    st.session_state.pop(f"confirm_delete_{mitarbeiter.id}", None)

    db.close()

    st.divider()
    
    st.subheader("👥 Mitarbeitende hinzufügen")
    # --- Form zum Hinzufügen ---
    with st.form("add_mitarbeiter_form"):
        name = st.text_input("Vorname")
        nachname = st.text_input("Nachname")
        farbe = st.color_picker("Farbe", "#FF9900")
        submitted = st.form_submit_button("Hinzufügen")

        if submitted:
            if name and nachname:
                db = SessionLocal()
                neuer_mitarbeiter = Mitarbeiter(name=name, nachname=nachname, farbe=farbe)
                try:
                    db.add(neuer_mitarbeiter)
                    db.commit()
                    st.success(f"{name} {nachname} wurde hinzugefügt ✅")
                    st.rerun()
                except SQLAlchemyError as e:
                    db.rollback()
                    st.error("Fehler beim Speichern")
                    st.exception(e)
                finally:
                    db.close()
            else:
                st.warning("Vor- und Nachname dürfen nicht leer sein.")

