import streamlit as st
from db.session import SessionLocal
from db.models import User
from utils.auth import verify_password

def login_view():
    st.title("🔐 Login")

    db = SessionLocal()
    users = db.query(User).all()
    db.close()

    usernames = [u.username for u in users]

    username = st.selectbox("Benutzername", usernames)  # 👈 dropdown instead of text_input
    password = st.text_input("Passwort", type="password")
    login_button = st.button("Login")

    if login_button:
        db = SessionLocal()
        user = db.query(User).filter(User.username == username).first()
        db.close()

        if user and verify_password(password, user.password_hash):
            st.session_state["username"] = user.username
            st.session_state["role"] = user.role
            st.success(f"Willkommen, {user.username}!")
            st.rerun()  # Refresh to update session state
        else:
            st.error("❌ Ungültiger Benutzername oder Passwort")

    return "username" in st.session_state
