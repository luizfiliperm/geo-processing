import streamlit as st
from ui.country_ui import render_country_page
from db_sqlite import init_db

# Inicializa o banco SQLite (cria tabelas se não existirem)
init_db()

# ------------------ Tela inicial ------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

def go_to(page_name):
    st.session_state.page = page_name

# Navbar / Home
if st.session_state.page == "home":
    st.title("Projeto Persistência Poliglota 🚀")
    st.subheader("Escolha uma opção:")

    if st.button("🌎 Gerenciar Países"):
        go_to("countries")

# Página de países
elif st.session_state.page == "countries":
    if st.button("⬅️ Voltar"):
        go_to("home")
    render_country_page()

# Futuro: Página de cidades
elif st.session_state.page == "cities":
    if st.button("⬅️ Voltar"):
        go_to("home")
    st.info("Página de cidades em desenvolvimento")
