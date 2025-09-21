import streamlit as st
from ui.country_ui import render_country_page
from ui.city_ui import render_city_page
from ui.form_local_ui import render_local_page
from ui.local_consulta_ui import render_consulta_page
from db_sqlite import init_db

# Inicializa o banco SQLite (cria tabelas se não existirem)
init_db()

# ------------------ Controle de página ------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

def go_to(page_name):
    st.session_state.page = page_name

# ------------------ Navbar / Home ------------------
if st.session_state.page == "home":
    st.title("Projeto Persistência Poliglota 🚀")
    st.subheader("Escolha uma opção:")

    if st.button("🌎 Gerenciar Países"):
        go_to("countries")
    if st.button("🏙️ Gerenciar Cidades"):
        go_to("cities")
    if st.button("📍 Gerenciar Locais"):
        go_to("locals")
    if st.button("🔎 Consultar Locais Próximos"):
        go_to("consulta_locais")

# ------------------ Página de Países ------------------
elif st.session_state.page == "countries":
    if st.button("⬅️ Voltar"):
        go_to("home")
    render_country_page()

# ------------------ Página de Cidades ------------------
elif st.session_state.page == "cities":
    if st.button("⬅️ Voltar"):
        go_to("home")
    render_city_page()

# ------------------ Página de Locais ------------------
elif st.session_state.page == "locals":
    if st.button("⬅️ Voltar"):
        go_to("home")
    render_local_page()

# ------------------ Página de Consulta de Locais ------------------
elif st.session_state.page == "consulta_locais":
    if st.button("⬅️ Voltar"):
        go_to("home")
    render_consulta_page()
