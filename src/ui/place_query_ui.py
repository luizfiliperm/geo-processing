import streamlit as st
import folium
import pandas as pd
from services.city_service import CityService
from streamlit_folium import st_folium
from geoprocessing import get_nearby_places


def render_query_page():
    st.title("🔎 Consulta de Locais Próximos")

    # Controle de estado
    if "lat" not in st.session_state:
        st.session_state.lat = -7.11532
    if "lon" not in st.session_state:
        st.session_state.lon = -34.861
    if "found_places" not in st.session_state:
        st.session_state.found_places = []

    # Carregar cidades do SQLite
    city_objects = CityService().get_all()
    city_options = ["Todas"] + [c.name for c in city_objects]

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
    for place in st.session_state.found_places:
        if "coordenadas" not in place:
            st.warning(f"⚠️ Local sem coordenadas: {place.get('nome_local', 'Sem nome')} - {place}")
            continue
        
        folium.Marker(
            [place["coordenadas"]["latitude"], place["coordenadas"]["longitude"]],
            popup=place.get("nome_local", "Sem nome"),
            tooltip=place.get("nome_local", "Sem nome"),
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)



    map_data = st_folium(m, width=700, height=400)

    if map_data and map_data.get("last_clicked"):
        st.session_state.lat = map_data["last_clicked"]["lat"]
        st.session_state.lon = map_data["last_clicked"]["lng"]
        st.info(f"📍 Latitude: {st.session_state.lat:.6f}, Longitude: {st.session_state.lon:.6f}")

    # ------------------ Filtros ------------------
    st.subheader("Filtros de busca")
    city_filter = st.selectbox("Filtrar por cidade (opcional)", city_options)
    radius_km = st.number_input("Raio em km", value=10, min_value=1)

    if st.button("🔍 Buscar Locais Próximos"):
        places = get_nearby_places(st.session_state.lat, st.session_state.lon, radius_km)

        if city_filter != "Todas":
            places = [p for p in places if p["cidade"] == city_filter]

        st.session_state.found_places = places  # salvar resultado na sessão

    # ------------------ Exibir resultados ------------------
    if st.session_state.found_places:
        places = st.session_state.found_places
        st.success(f"{len(places)} locais encontrados dentro de {radius_km} km")

        # Tabela
        df = pd.DataFrame([{
        "Nome": p.get("nome_local", "Sem nome"),
        "Cidade": p.get("cidade", "Desconhecida"),
        "Latitude": p.get("coordenadas", {}).get("latitude", None),
        "Longitude": p.get("coordenadas", {}).get("longitude", None),
        "Descrição": p.get("descricao", "")
    } for p in places])

        # Garantir que _id não apareça
        if "_id" in df.columns:
            df = df.drop(columns=["_id"])

        st.dataframe(df)
