# views/schichtabtausch.py

import streamlit as st
from sqlalchemy.orm import Session
from db.session import SessionLocal
from db.models import Urlaub, Schicht, Mitarbeiter
from datetime import date

def schichtabtausch_view():
    st.header("🔁 Schichtabtausch")

    db: Session = SessionLocal()

    # Hole alle bestätigten Urlaube
    bestaetigte_urlaube = db.query(Urlaub).filter(Urlaub.status == "bestätigt").all()

    if not bestaetigte_urlaube:
        st.info("Keine bestätigten Urlaube gefunden.")
        db.close()
        return

    # Hole alle Mitarbeitenden
    mitarbeiter_liste = db.query(Mitarbeiter).all()
    mitarbeiter_map = {m.id: f"{m.name} {m.nachname}" for m in mitarbeiter_liste}

    st.subheader("Zu tauschende Schichten (wegen Urlaub)")

    for urlaub in bestaetigte_urlaube:
        # Alle Schichten dieses Mitarbeiters während seines Urlaubs
        schichten = db.query(Schicht).filter(
            Schicht.mitarbeiter_id == urlaub.mitarbeiter_id,
            Schicht.datum >= urlaub.von,
            Schicht.datum <= urlaub.bis
        ).all()

        for schicht in schichten:
            col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 3, 2])
            col1.write(mitarbeiter_map[schicht.mitarbeiter_id])
            col2.write(schicht.datum.strftime("%d.%m.%Y"))
            col3.write(f"{schicht.von.strftime('%H:%M')} – {schicht.bis.strftime('%H:%M')}")
            
            # Auswahl für neuen Mitarbeiter
            andere_mitarbeiter = [m for m in mitarbeiter_liste if m.id != schicht.mitarbeiter_id]
            auswahl = col4.selectbox(
                f"Vertretung für Schicht {schicht.id}",
                ["—"] + [f"{m.name} {m.nachname}" for m in andere_mitarbeiter],
                key=f"vertretung_{schicht.id}"
            )

            if auswahl != "—":
                if col5.button("💾 Übernehmen", key=f"save_{schicht.id}"):
                    neuer_mitarbeiter_id = next(
                        (m.id for m in andere_mitarbeiter if f"{m.name} {m.nachname}" == auswahl),
                        None
                    )
                    if neuer_mitarbeiter_id:
                        schicht.mitarbeiter_id = neuer_mitarbeiter_id
                        db.commit()
                        st.success(f"Schicht {schicht.id} erfolgreich übertragen an {auswahl}")
                        st.rerun()

    db.close()
