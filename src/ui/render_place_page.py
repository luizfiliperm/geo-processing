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
    if "edit_nome" not in st.session_state:
        st.session_state.edit_nome = ""
    if "edit_cidade_index" not in st.session_state:
        st.session_state.edit_cidade_index = 0
    if "edit_descricao" not in st.session_state:
        st.session_state.edit_descricao = ""

    # ------------------ Inserir / Editar Local ------------------
    st.subheader("Adicionar / Editar Local")
    nome = st.text_input("Nome do Local", value=st.session_state.edit_nome)
    
    cidades = get_cities()
    if not cidades:
        st.warning("Não há cidades cadastradas. Adicione primeiro no SQLite!")
        return
    cidade_selecionada = st.selectbox(
        "Cidade",
        [c['name'] for c in cidades],
        index=st.session_state.edit_cidade_index
    )

    latitude = st.number_input("Latitude", value=st.session_state.lat, format="%.6f")
    longitude = st.number_input("Longitude", value=st.session_state.lon, format="%.6f")
    descricao = st.text_area("Descrição", value=st.session_state.edit_descricao)

    if st.button("Salvar Local"):
        collection = get_collection()
        if st.session_state.edit_local_id:
            # Editar local
            collection.update_one(
                {"_id": st.session_state.edit_local_id},
                {"$set": {
                    "nome_local": nome,
                    "cidade": cidade_selecionada,
                    "coordenadas": {"latitude": latitude, "longitude": longitude},
                    "descricao": descricao
                }}
            )
            st.success(f"Local '{nome}' atualizado com sucesso!")
            st.session_state.edit_local_id = None
        else:
            # Adicionar novo local
            collection.insert_one({
                "nome_local": nome,
                "cidade": cidade_selecionada,
                "coordenadas": {"latitude": latitude, "longitude": longitude},
                "descricao": descricao
            })
            st.success(f"Local '{nome}' adicionado com sucesso!")

        # Resetar session_state
        st.session_state.edit_nome = ""
        st.session_state.edit_cidade_index = 0
        st.session_state.edit_descricao = ""
        st.session_state.lat = -7.11532
        st.session_state.lon = -34.861

    st.markdown("---")

    # ------------------ Consulta de Locais ------------------
    st.subheader("Consultar Locais Próximos")
    cidade_filtro = st.selectbox("Filtrar por cidade (opcional)", ["Todas"] + [c['name'] for c in cidades])
    lat_filtro = st.number_input("Latitude para proximidade", format="%.6f", value=st.session_state.lat)
    lon_filtro = st.number_input("Longitude para proximidade", format="%.6f", value=st.session_state.lon)
    raio_km = st.number_input("Raio em km", value=10, min_value=1)

    if st.button("Buscar Locais Próximos"):
        if lat_filtro is not None and lon_filtro is not None:
            locais = get_nearby_places(lat_filtro, lon_filtro, raio_km)
            if cidade_filtro != "Todas":
                locais = [l for l in locais if l["cidade"] == cidade_filtro]

            if locais:
                st.success(f"{len(locais)} locais encontrados dentro de {raio_km} km")
                
                # Exibir em tabela
                df = pd.DataFrame([{
                    "Nome": l["nome_local"],
                    "Cidade": l["cidade"],
                    "Latitude": l["coordenadas"]["latitude"],
                    "Longitude": l["coordenadas"]["longitude"],
                    "Descrição": l.get("descricao", "")
                } for l in locais])
                st.dataframe(df)

                # Exibir no mapa
                mapa = folium.Map(location=[lat_filtro, lon_filtro], zoom_start=12)
                folium.Marker([lat_filtro, lon_filtro], tooltip="Ponto de referência", icon=folium.Icon(color="red")).add_to(mapa)

                for l in locais:
                    folium.Marker(
                        [l["coordenadas"]["latitude"], l["coordenadas"]["longitude"]],
                        tooltip=l["nome_local"]
                    ).add_to(mapa)

                st_folium(mapa, width=700, height=500)
            else:
                st.warning("Nenhum local encontrado nesse raio.")
        else:
            st.warning("Informe a latitude e longitude para buscar locais próximos.")
