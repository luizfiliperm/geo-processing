import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from db_mongo import get_collection
from db_sqlite import get_cities
from geoprocessing import get_nearby_places


def render_local_page():
    st.header("📍 Gerenciar Locais")

    # ------------------ Inicialização do session_state ------------------
    if "lat" not in st.session_state:
        st.session_state.lat = -7.11532
    if "lon" not in st.session_state:
        st.session_state.lon = -34.861
    if "edit_local_id" not in st.session_state:
        st.session_state.edit_local_id = None
    if "edit_name" not in st.session_state:
        st.session_state.edit_name = ""
    if "edit_city_index" not in st.session_state:
        st.session_state.edit_city_index = 0
    if "edit_description" not in st.session_state:
        st.session_state.edit_description = ""

    # ------------------ Inserir / Editar Local ------------------
    st.subheader("Adicionar / Editar Local")
    name = st.text_input("Nome do Local", value=st.session_state.edit_name)
    
    cities = get_cities()
    if not cities:
        st.warning("Não há cidades cadastradas. Adicione primeiro no SQLite!")
        return
    selected_city = st.selectbox(
        "Cidade",
        [c['name'] for c in cities],
        index=st.session_state.edit_city_index
    )

    latitude = st.number_input("Latitude", value=st.session_state.lat, format="%.6f")
    longitude = st.number_input("Longitude", value=st.session_state.lon, format="%.6f")
    description = st.text_area("Descrição", value=st.session_state.edit_description)

    if st.button("Salvar Local"):
        collection = get_collection()
        if st.session_state.edit_local_id:
            # Editar local
            collection.update_one(
                {"_id": st.session_state.edit_local_id},
                {"$set": {
                    "nome_local": name,
                    "cidade": selected_city,
                    "coordenadas": {"latitude": latitude, "longitude": longitude},
                    "descricao": description
                }}
            )
            st.success(f"Local '{name}' atualizado com sucesso!")
            st.session_state.edit_local_id = None
        else:
            # Adicionar novo local
            collection.insert_one({
                "nome_local": name,
                "cidade": selected_city,
                "coordenadas": {"latitude": latitude, "longitude": longitude},
                "descricao": description
            })
            st.success(f"Local '{name}' adicionado com sucesso!")

        # Resetar session_state
        st.session_state.edit_name = ""
        st.session_state.edit_city_index = 0
        st.session_state.edit_description = ""
        st.session_state.lat = -7.11532
        st.session_state.lon = -34.861

    st.markdown("---")

    # ------------------ Consulta de Locais ------------------
    st.subheader("Consultar Locais Próximos")
    city_filter = st.selectbox("Filtrar por cidade (opcional)", ["Todas"] + [c['name'] for c in cities])
    lat_filter = st.number_input("Latitude para proximidade", format="%.6f", value=st.session_state.lat)
    lon_filter = st.number_input("Longitude para proximidade", format="%.6f", value=st.session_state.lon)
    radius_km = st.number_input("Raio em km", value=10, min_value=1)

    if st.button("Buscar Locais Próximos"):
        if lat_filter is not None and lon_filter is not None:
            places = get_nearby_places(lat_filter, lon_filter, radius_km)
            if city_filter != "Todas":
                places = [l for l in places if l["cidade"] == city_filter]

            if places:
                st.success(f"{len(places)} locais encontrados dentro de {radius_km} km")
                
                # Exibir em tabela
                df = pd.DataFrame([{
                    "Nome": l["nome_local"],
                    "Cidade": l["cidade"],
                    "Latitude": l["coordenadas"]["latitude"],
                    "Longitude": l["coordenadas"]["longitude"],
                    "Descrição": l.get("descricao", "")
                } for l in places])
                st.dataframe(df)

                # Exibir no mapa
                map_ = folium.Map(location=[lat_filter, lon_filter], zoom_start=12)
                folium.Marker([lat_filter, lon_filter], tooltip="Ponto de referência", icon=folium.Icon(color="red")).add_to(map_)

                for l in places:
                    folium.Marker(
                        [l["coordenadas"]["latitude"], l["coordenadas"]["longitude"]],
                        tooltip=l["nome_local"]
                    ).add_to(map_)

                st_folium(map_, width=700, height=500)
            else:
                st.warning("Nenhum local encontrado nesse raio.")
        else:
            st.warning("Informe a latitude e longitude para buscar locais próximos.")
