import streamlit as st
from sqlalchemy.orm import Session
from db.models import Mitarbeiter, Urlaub
from db.session import SessionLocal
from datetime import date

def mitarbeiter_view():
    st.header("👤 Mitarbeiter hinzufügen")

    with st.form("add_mitarbeiter_form"):
        name = st.text_input("Name des Mitarbeiters")
        farbe = st.color_picker("Farbe", "#FF9900")
        submitted = st.form_submit_button("Hinzufügen")

        if submitted:
            if name:
                db = SessionLocal()
                neuer_mitarbeiter = Mitarbeiter(name=name, farbe=farbe)
                try:
                    db.add(neuer_mitarbeiter)
                    db.commit()
                    st.success(f"{name} wurde hinzugefügt ✅")
                except SQLAlchemyError as e:
                    db.rollback()
                    st.error("Fehler beim Speichern")
                    st.exception(e)
                finally:
                    db.close()
            else:
                st.warning("Name darf nicht leer sein.")

    st.divider()
    st.subheader("📋 Bestehende Mitarbeiter")
    db = SessionLocal()
    mitarbeiter_liste = db.query(Mitarbeiter).all()
    db.close()

    for m in mitarbeiter_liste:
        st.markdown(f"- <span style='color:{m.farbe}'>{m.name}</span>", unsafe_allow_html=True)