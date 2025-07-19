from db.session import engine
from db.models import Base
import streamlit as st
from views.urlaub import urlaub_view
from views.mitarbeiter import mitarbeiter_view
from views.dashboard import dashboard_view
from views.oeffnungszeiten import oeffnungszeiten_view
from views.login import login_view
from db.session import SessionLocal
from db.models import User
from utils.auth import verify_password

Base.metadata.create_all(bind=engine)
db = SessionLocal()
for user in db.query(User).all():
    print(user.username, user.role, user.password_hash)
db.close()


