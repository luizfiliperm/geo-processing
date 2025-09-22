import streamlit as st
import folium
import pandas as pd
from streamlit_folium import st_folium
from geoprocessing import get_nearby_places
from db_sqlite import get_cities

def render_consulta_page():
    st.title("🔎 Consulta de Locais Próximos")

    # Controle de estado
    if "lat" not in st.session_state:
        st.session_state.lat = -7.11532
    if "lon" not in st.session_state:
        st.session_state.lon = -34.861
    if "locais_encontrados" not in st.session_state:
        st.session_state.locais_encontrados = []

    # Carregar cidades do SQLite
    cidades = get_cities()
    city_options = ["Todas"] + [c["name"] for c in cidades]

    # ------------------ Mapa interativo ------------------
    st.markdown("**Clique no mapa para escolher a referência de proximidade**")
    m = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=12)

    folium.CircleMarker(
        location=[st.session_state.lat, st.session_state.lon],
        radius=8,
        color="red",
        fill=True,
        fill_color="red",
        fill_opacity=0.7,
        tooltip="Ponto de referência"
    ).add_to(m)

    # Se já tiver locais encontrados, desenhar no mapa
    for l in st.session_state.locais_encontrados:
        folium.Marker(
            [l["coordenadas"]["latitude"], l["coordenadas"]["longitude"]],
            popup=l["nome_local"],
            tooltip=l["nome_local"],
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

    map_data = st_folium(m, width=700, height=400)

    if map_data and map_data.get("last_clicked"):
        st.session_state.lat = map_data["last_clicked"]["lat"]
        st.session_state.lon = map_data["last_clicked"]["lng"]
        st.info(f"📍 Latitude: {st.session_state.lat:.6f}, Longitude: {st.session_state.lon:.6f}")

    # ------------------ Filtros ------------------
    st.subheader("Filtros de busca")
    cidade_filtro = st.selectbox("Filtrar por cidade (opcional)", city_options)
    raio_km = st.number_input("Raio em km", value=10, min_value=1)

    if st.button("🔍 Buscar Locais Próximos"):
        locais = get_nearby_places(st.session_state.lat, st.session_state.lon, raio_km)

        if cidade_filtro != "Todas":
            locais = [l for l in locais if l["cidade"] == cidade_filtro]

        st.session_state.locais_encontrados = locais  # salvar resultado na sessão

    # ------------------ Exibir resultados ------------------
    if st.session_state.locais_encontrados:
        locais = st.session_state.locais_encontrados
        st.success(f"{len(locais)} locais encontrados dentro de {raio_km} km")

        # Tabela
        df = pd.DataFrame([{
            "Nome": l["nome_local"],
            "Cidade": l["cidade"],
            "Latitude": l["coordenadas"]["latitude"],
            "Longitude": l["coordenadas"]["longitude"],
            "Descrição": l.get("descricao", "")
        } for l in locais])
        # Garantir que _id não apareça
        if "_id" in df.columns:
            df = df.drop(columns=["_id"])

        st.dataframe(df)
