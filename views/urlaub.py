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

    name_map = {f"{m.name} {m.nachname}": m.id for m in mitarbeiter_liste}

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
            col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 2])
            col1.write(f"👤 {eintrag.mitarbeiter.name} {eintrag.mitarbeiter.nachname}")
            col2.write(eintrag.von.strftime("%d.%m.%Y"))
            col3.write(eintrag.bis.strftime("%d.%m.%Y"))
            col4.write(f"📌 {eintrag.status}")

            if col5.button("✏️ Bearbeiten", key=f"edit_{eintrag.id}"):
                with st.form(f"edit_form_{eintrag.id}", clear_on_submit=False):
                    neue_von = st.date_input("Neues Von", eintrag.von, key=f"von_{eintrag.id}")
                    neue_bis = st.date_input("Neues Bis", eintrag.bis, key=f"bis_{eintrag.id}")
                    neuer_status = st.selectbox("Neuer Status", ["offen", "bestätigt", "abgelehnt"], index=["offen", "bestätigt", "abgelehnt"].index(eintrag.status), key=f"status_{eintrag.id}")
                    speichern = st.form_submit_button("Änderungen speichern")

                    if speichern:
                        eintrag_aktuell = db.query(Urlaub).get(eintrag.id)
                        eintrag_aktuell.von = neue_von
                        eintrag_aktuell.bis = neue_bis
                        eintrag_aktuell.status = neuer_status
                        db.commit()
                        st.rerun()
    else:
        st.info("Keine Urlaube erfasst.")

    db.close()
