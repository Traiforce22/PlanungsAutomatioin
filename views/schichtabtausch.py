# views/schichtabtausch.py

import streamlit as st
from sqlalchemy.orm import Session
from db.session import SessionLocal
from db.models import Urlaub, Mitarbeiter, WoechentlicheSchicht, Schicht
from datetime import date, timedelta

def schichtabtausch_view():
    st.header("🔁 Schichtabtausch")

    db: Session = SessionLocal()

    # Hole alle bestätigten Urlaube
    bestaetigte_urlaube = db.query(Urlaub).filter(Urlaub.status == "bestätigt").all()
    if not bestaetigte_urlaube:
        st.info("Keine bestätigten Urlaube gefunden.")
        db.close()
        return

    mitarbeiter_liste = db.query(Mitarbeiter).all()
    mitarbeiter_map = {m.id: f"{m.name} {m.nachname}" for m in mitarbeiter_liste}
    wochenschichten = db.query(WoechentlicheSchicht).all()

    st.subheader("Zu tauschende Schichten (aus Wochenschicht während Urlaub)")

    for urlaub in bestaetigte_urlaube:
        urlaubstage = (urlaub.bis - urlaub.von).days + 1
        urlaub_mitarbeiter = next((m for m in mitarbeiter_liste if m.id == urlaub.mitarbeiter_id), None)
        if not urlaub_mitarbeiter:
            continue

        mitarbeiter_wochenplan = [ws for ws in wochenschichten if ws.mitarbeiter_id == urlaub.mitarbeiter_id]

        for i in range(urlaubstage):
            aktuelles_datum = urlaub.von + timedelta(days=i)
            wochentag = aktuelles_datum.strftime("%A")  # z.B. "Monday"
            wochentag_de = {
                "Monday": "Montag",
                "Tuesday": "Dienstag",
                "Wednesday": "Mittwoch",
                "Thursday": "Donnerstag",
                "Friday": "Freitag",
                "Saturday": "Samstag",
                "Sunday": "Sonntag"
            }[wochentag]

            # Hat die Person an diesem Tag einen Wochenschicht-Eintrag?
            passende_schichten = [ws for ws in mitarbeiter_wochenplan if ws.wochentag == wochentag_de]
            for ws in passende_schichten:
                col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 3, 2])
                col1.write(f"{urlaub_mitarbeiter.name} {urlaub_mitarbeiter.nachname}")
                col2.write(aktuelles_datum.strftime("%d.%m.%Y"))
                col3.write(f"{ws.von.strftime('%H:%M')} – {ws.bis.strftime('%H:%M')}")

                andere_mitarbeiter = [m for m in mitarbeiter_liste if m.id != urlaub.mitarbeiter_id]
                auswahl = col4.selectbox(
                    f"Vertretung {urlaub.id}_{aktuelles_datum}",
                    ["—"] + [f"{m.name} {m.nachname}" for m in andere_mitarbeiter],
                    key=f"vertretung_{urlaub.id}_{aktuelles_datum}"
                )

                if auswahl != "—":
                    if col5.button("💾 Übernehmen", key=f"save_{urlaub.id}_{aktuelles_datum}"):
                        neuer_mitarbeiter_id = next(
                            (m.id for m in andere_mitarbeiter if f"{m.name} {m.nachname}" == auswahl),
                            None
                        )
                        if neuer_mitarbeiter_id:
                            neue_schicht = Schicht(
                                mitarbeiter_id=neuer_mitarbeiter_id,
                                datum=aktuelles_datum,
                                von=ws.von,
                                bis=ws.bis,
                                editable=True
                            )
                            db.add(neue_schicht)
                            db.commit()
                            st.success(f"Schicht am {aktuelles_datum.strftime('%d.%m.%Y')} übernommen von {auswahl}")
                            st.rerun()

    db.close()
