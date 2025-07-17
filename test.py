import streamlit as st
st.header("Testseite")
st.write("Dies ist eine Testseite für die PlanungsAutomation App.")
st.sidebar.title("Navigation")

option = st.sidebar.selectbox("Menü", ["Start", "Einstellungen", "Über"])
if option == "Start":
    st.title("Willkommen")
    col1, col2 = st.columns(2)
    col1.write("Linke Spalte")
    col2.write("Rechte Spalte")
elif option == "Einstellungen":
    st.write("Hier kannst du Einstellungen vornehmen.")
else:
    st.write("Über die App...")
