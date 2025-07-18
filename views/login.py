import streamlit as st
import streamlit_authenticator as stauth
from db.session import SessionLocal
from db.models import User
from utils.auth import verify_password

def login_view():
    st.title("🔐 Login")

    db = SessionLocal()
    users_db = db.query(User).all()

    # Prepare dict for stauth (username: {"name": username, "password": hashed_pw})
    credentials = {
        u.username: {"name": u.username, "password": u.password_hash}
        for u in users_db
    }
    db.close()

    authenticator = stauth.Authenticate(
        credentials,
        "some_cookie_name",
        "some_signature_key",
        cookie_expiry_days=30,
        preauthorized=None,
    )

    name, authentication_status, username = authenticator.login("Login", "main")

    if authentication_status:
        st.success(f"Willkommen, {name}!")
        # Save user role in session state
        user_role = next((u.role for u in users_db if u.username == username), "user")
        st.session_state["username"] = username
        st.session_state["role"] = user_role
        return True
    elif authentication_status is False:
        st.error("Falscher Benutzername oder Passwort.")
    else:
        st.warning("Bitte anmelden.")

    return False
