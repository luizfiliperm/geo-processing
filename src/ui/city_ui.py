# src/ui/city_ui.py
import streamlit as st
from services.city_service import CityService
from services.country_service import CountryService
from domains.city import City
from domains.state_enum import State
import folium
from streamlit_folium import st_folium

def render_city_page():
    st.title("Gestão de Cidades 🏙️")
    city_service = CityService()
    country_service = CountryService()

    # Controle de edição
    if "edit_city_id" not in st.session_state:
        st.session_state.edit_city_id = None
    if "refresh_cities" not in st.session_state:
        st.session_state.refresh_cities = True
    if "lat" not in st.session_state:
        st.session_state.lat = -7.11532  # João Pessoa como default
    if "lon" not in st.session_state:
        st.session_state.lon = -34.861

    countries = country_service.get_all()
    country_options = {c.name: c.id for c in countries}
    state_options = [s.name for s in State]

    # ------------------ Mapa interativo ------------------
    st.markdown("**Clique no mapa para selecionar a localização da cidade**")

    # Centraliza no ponto selecionado
    m = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=12)

    # Marcador verde indicando seleção atual
    folium.CircleMarker(
        location=[st.session_state.lat, st.session_state.lon],
        radius=8,
        color='green',
        fill=True,
        fill_color='green',
        fill_opacity=0.7,
        tooltip="Cidade selecionada"
    ).add_to(m)

    # Renderiza mapa
    map_data = st_folium(m, width=700, height=400)

    # Captura clique do usuário
    if map_data and map_data.get("last_clicked"):
        st.session_state.lat = map_data["last_clicked"]["lat"]
        st.session_state.lon = map_data["last_clicked"]["lng"]
        st.info(f"Latitude: {st.session_state.lat:.6f}, Longitude: {st.session_state.lon:.6f}")


    # ------------------ Formulário de criação/edição ------------------
    with st.form("city_form"):
        if st.session_state.edit_city_id:
            city_to_edit = city_service.get_by_id(st.session_state.edit_city_id)
            name = st.text_input("Nome da cidade", city_to_edit.name)
            state_index = state_options.index(city_to_edit.state.name) if city_to_edit.state else 0
            state_name = st.selectbox("Estado", state_options, index=state_index)
            country_name = next(k for k, v in country_options.items() if v == city_to_edit.country_id)
            country_selected = st.selectbox("País", list(country_options.keys()),
                                            index=list(country_options.keys()).index(country_name))
            button_label = "Atualizar cidade"
        else:
            name = st.text_input("Nome da cidade")
            state_name = st.selectbox("Estado", state_options)
            country_selected = st.selectbox("País", list(country_options.keys()))
            button_label = "Salvar cidade"

        submitted = st.form_submit_button(button_label)
        if submitted:
            try:
                city = City(
                    id=st.session_state.edit_city_id,
                    name=name,
                    state=State[state_name],
                    country_id=country_options[country_selected],
                    latitude=st.session_state.lat,
                    longitude=st.session_state.lon
                )
                city_service.validate(city)
                city_service.save(city)
                st.success(f"Cidade salva com sucesso!")
                st.session_state.edit_city_id = None
                st.session_state.refresh_cities = True
            except Exception as e:
                st.error(f"Erro ao salvar cidade: {e}")

    # ------------------ Lista de cidades ------------------
    cities = city_service.get_all()
    st.session_state.refresh_cities = False

    st.subheader("Cidades cadastradas")
    for c in cities:
        col1, col2, col3 = st.columns([4, 1, 1])
        country_name = next((k for k, v in country_options.items() if v == c.country_id), "Desconhecido")
        col1.write(f"{c.name}, {c.state.value if c.state else '—'}, {country_name}")

        # Botão editar
        if col2.button("✏️", key=f"edit_{c.id}"):
            st.session_state.edit_city_id = c.id
            st.session_state.lat = c.latitude if c.latitude else st.session_state.lat
            st.session_state.lon = c.longitude if c.longitude else st.session_state.lon

        # Botão apagar com confirmação
        if col3.button("🗑️", key=f"delete_{c.id}"):
            st.session_state.confirm_delete_city_id = c.id

        # Confirmação Sim/Não
        if "confirm_delete_city_id" in st.session_state and st.session_state.confirm_delete_city_id == c.id:
            st.warning(f"⚠️ Você realmente quer deletar a cidade {c.name}?")
            col_confirm1, col_confirm2 = st.columns([1, 1])
            if col_confirm1.button("✅ Sim", key=f"confirm_yes_{c.id}"):
                city_service.delete(c.id)
                st.success(f"Cidade {c.name} excluída!")
                st.session_state.refresh_cities = True
                del st.session_state.confirm_delete_city_id
            if col_confirm2.button("❌ Não", key=f"confirm_no_{c.id}"):
                del st.session_state.confirm_delete_city_id
