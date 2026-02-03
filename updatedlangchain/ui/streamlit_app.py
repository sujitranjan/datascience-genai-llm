import streamlit as st
import requests

st.title("Agentic AI Assistant")

# ---- LOGIN ----
if "session_id" not in st.session_state:
    username = st.text_input("Enter username")

    if st.button("Login") and username:
        res = requests.post(
            "http://localhost:8000/login",## like phone number#“The same machine I’m running on”#8000-Port where FastAPI is listening, / login is the route
            params={"username": username}
        )

        st.session_state.session_id = res.json()["session_id"]
        st.success("Logged in!")

# ---- CHAT ----
if "session_id" in st.session_state:
    message = st.text_input("Ask something")

    if st.button("Send") and message:
        response = requests.post(
            "http://localhost:8000/chat",
            params={
                "session_id": st.session_state.session_id,
                "message": message
            }
        )
        st.write(response.json()["response"])



##lambda is klitchen , fastapi is the menu-
# Why this is actually GOOD design

# If Streamlit had to import app.py:

# Both would run in the same process

# State would mix

# Scaling would be impossible

# HTTP gives you:

# Decoupling

# Language-agnostic communication

# Easy deployment
