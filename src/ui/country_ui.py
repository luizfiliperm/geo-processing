# src/ui/country_ui.py
import streamlit as st
from services.country_service import CountryService
from domains.country import Country

def render_country_page():
    st.title("Gestão de Países 🌎")
    service = CountryService()

    # ------------------ Controle de sessão ------------------
    if "edit_country_id" not in st.session_state:
        st.session_state.edit_country_id = None
    if "refresh" not in st.session_state:
        st.session_state.refresh = True

    # ------------------ Formulário de criação/edição ------------------
    with st.form("country_form"):
        if st.session_state.edit_country_id:
            country_to_edit = service.get_by_id(st.session_state.edit_country_id)
            name = st.text_input("Nome do país", country_to_edit.name)
            iso_code = st.text_input("Código ISO (2 letras)", country_to_edit.iso_code).upper()
            button_label = "Atualizar país"
        else:
            name = st.text_input("Nome do país")
            iso_code = st.text_input("Código ISO (2 letras)").upper()
            button_label = "Salvar país"

        submitted = st.form_submit_button(button_label)
        if submitted:
            try:
                country = Country(
                    id=st.session_state.edit_country_id,
                    name=name,
                    iso_code=iso_code
                )
                saved = service.save(country)
                st.success(f"País salvo com sucesso! {saved}")
                st.session_state.edit_country_id = None
                st.session_state.refresh = True  # força atualização da lista
            except Exception as e:
                st.error(f"Erro: {e}")

    # ------------------ Lista de países ------------------
    if st.session_state.refresh:
        countries = service.get_all()
        st.session_state.refresh = False
    else:
        countries = service.get_all()

    st.subheader("Países cadastrados")
    for c in countries:
        col1, col2, col3 = st.columns([4, 1, 1])
        col1.write(f"{c.name} ({c.iso_code})")  # não mostra ID

        # Botão editar
        if col2.button("✏️", key=f"edit_{c.id}"):
            st.session_state.edit_country_id = c.id

        # Botão apagar com confirmação
        if col3.button("🗑️", key=f"delete_{c.id}"):
            st.session_state.confirm_delete_id = c.id

        # Confirmação Sim/Não
        if "confirm_delete_id" in st.session_state and st.session_state.confirm_delete_id == c.id:
            st.warning("⚠️ Você realmente quer deletar este país?")
            col_confirm1, col_confirm2 = st.columns([1, 1])
            if col_confirm1.button("✅ Sim", key=f"confirm_yes_{c.id}"):
                service.delete(c.id)
                st.success(f"País {c.name} excluído!")
                st.session_state.refresh = True
                del st.session_state.confirm_delete_id
            if col_confirm2.button("❌ Não", key=f"confirm_no_{c.id}"):
                del st.session_state.confirm_delete_id
