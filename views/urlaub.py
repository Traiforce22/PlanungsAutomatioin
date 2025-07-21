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
        # Status wird standardmäßig auf 'offen' gesetzt
        status = "offen"
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
            st.rerun()

    # Bestehende Urlaube anzeigen, sortiert nach 'von'-Datum
    urlaube = db.query(Urlaub).order_by(Urlaub.von).all()
    if urlaube:
        st.subheader("Alle Urlaube")
        for eintrag in urlaube:
            col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 1, 1])
            col1.write(f"👤 {eintrag.mitarbeiter.name} {eintrag.mitarbeiter.nachname}")
            col2.write(eintrag.von.strftime("%d.%m.%Y"))
            col3.write(eintrag.bis.strftime("%d.%m.%Y"))
            col4.write(f"📌 {eintrag.status}")

            def enable_edit_mode(eintrags_id):
                st.session_state[f"edit_{eintrags_id}"] = True

            def cancel_edit_mode(eintrags_id):
                st.session_state[f"edit_{eintrags_id}"] = False

            col5.button("✏️", key=f"edit_btn_{eintrag.id}", on_click=enable_edit_mode, args=(eintrag.id,))

            if st.session_state.get(f"edit_{eintrag.id}", False):
                with st.form(f"edit_form_{eintrag.id}", clear_on_submit=False):
                    neue_von = st.date_input("Neues Von", eintrag.von, key=f"von_{eintrag.id}")
                    neue_bis = st.date_input("Neues Bis", eintrag.bis, key=f"bis_{eintrag.id}")

                    # Nur Admins dürfen den Status ändern
                    if st.session_state.get("role") == "admin":
                        neuer_status = st.selectbox(
                            "Neuer Status",
                            ["offen", "bestätigt", "abgelehnt"],
                            index=["offen", "bestätigt", "abgelehnt"].index(eintrag.status),
                            key=f"status_{eintrag.id}"
                        )
                    else:
                        neuer_status = eintrag.status

                    col_save, col_cancel = st.columns(2)
                    speichern = col_save.form_submit_button("💾 Speichern")
                    abbrechen = col_cancel.form_submit_button("❌ Schliessen")

                    if speichern:
                        eintrag_aktuell = db.query(Urlaub).get(eintrag.id)

                        # Wenn der Status bereits bestätigt ist, Admin muss doppelt bestätigen Ablehnung
                        if (
                            eintrag_aktuell.status == "bestätigt"
                            and neuer_status != "bestätigt"
                            and st.session_state.get("role") == "admin"
                        ):
                            if "confirm_unapprove" not in st.session_state:
                                st.warning("⚠️ Bestätigter Urlaub. Klicken Sie nochmal auf Speichern zur Bestätigung der Änderung.")
                                st.session_state["confirm_unapprove"] = True
                                st.stop()
                            else:
                                del st.session_state["confirm_unapprove"]

                        eintrag_aktuell.von = neue_von
                        eintrag_aktuell.bis = neue_bis
                        eintrag_aktuell.status = neuer_status
                        db.commit()
                        st.success("Urlaub geupdated.")
                        st.rerun()

                    if abbrechen:
                        cancel_edit_mode(eintrag.id)
                        st.rerun()
    else:
        st.info("Keine Urlaube erfasst.")

    db.close()
