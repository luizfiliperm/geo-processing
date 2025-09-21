# ui/local_ui.py
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from db_mongo import get_collection
from db_sqlite import get_cities
from geoprocessamento import locais_proximos

def render_local_page():
    st.header("📍 Gerenciar Locais")

    # ------------------ Inserir Novo Local ------------------
    st.subheader("Adicionar Novo Local")
    nome = st.text_input("Nome do Local")
    
    cidades = get_cities()
    if cidades:
        cidade_selecionada = st.selectbox("Cidade", [c['name'] for c in cidades])
    else:
        st.warning("Não há cidades cadastradas. Adicione primeiro no SQLite!")
        return
    
    latitude = st.number_input("Latitude", format="%.6f")
    longitude = st.number_input("Longitude", format="%.6f")
    descricao = st.text_area("Descrição")

    if st.button("Adicionar Local"):
        if nome and cidade_selecionada:
            collection = get_collection()
            collection.insert_one({
                "nome_local": nome,
                "cidade": cidade_selecionada,
                "coordenadas": {"latitude": latitude, "longitude": longitude},
                "descricao": descricao
            })
            st.success(f"Local '{nome}' adicionado com sucesso!")
        else:
            st.warning("Preencha todos os campos obrigatórios.")

    st.markdown("---")

    # ------------------ Consulta de Locais ------------------
    st.subheader("Consultar Locais Próximos")
    cidade_filtro = st.selectbox("Filtrar por cidade (opcional)", ["Todas"] + [c['name'] for c in cidades])
    lat_filtro = st.number_input("Latitude para proximidade", format="%.6f")
    lon_filtro = st.number_input("Longitude para proximidade", format="%.6f")
    raio_km = st.number_input("Raio em km", value=10, min_value=1)

    if st.button("Buscar Locais Próximos"):
        if lat_filtro and lon_filtro:
            locais = locais_proximos(lat_filtro, lon_filtro, raio_km)
            
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
