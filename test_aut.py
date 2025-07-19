import streamlit as st
import streamlit_authenticator as stauth

credentials = {
    "usernames": {
        "user1": {
            "name": "User One",
            "password": "$2b$12$abcxyzabcxyzabcxyzabcxyzabcxyzabcxyzabcxyzabcxyzabcxyzabcx",  # Use valid bcrypt hash here
            "role": "user"
        }
    }
}

authenticator = stauth.Authenticate(credentials, "cookie_name", "signature_key", cookie_expiry_days=30)
name, authentication_status, username = authenticator.login('Login', 'sidebar')

if authentication_status:
    st.write(f"Welcome {name}")
else:
    st.write("Please log in")
