import streamlit as st
import folium
from services.local_service import LocalService
from streamlit_folium import st_folium
from db_mongo import get_collection
from db_sqlite import get_cities

def render_local_page():
    st.header("📍 Gerenciar Locais")

    # ------------------ Sessão do mapa ------------------
    if "lat" not in st.session_state:
        st.session_state.lat = -7.11532
    if "lon" not in st.session_state:
        st.session_state.lon = -34.861
    if "edit_local_id" not in st.session_state:
        st.session_state.edit_local_id = None

    st.markdown("**Clique no mapa para selecionar a localização do local**")
    m = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=12)
    folium.CircleMarker(
        location=[st.session_state.lat, st.session_state.lon],
        radius=8,
        color='green',
        fill=True,
        fill_color='green',
        fill_opacity=0.7,
        tooltip="Local selecionado"
    ).add_to(m)

    map_data = st_folium(m, width=700, height=400)
    if map_data and map_data.get("last_clicked"):
        st.session_state.lat = map_data["last_clicked"]["lat"]
        st.session_state.lon = map_data["last_clicked"]["lng"]

    # ------------------ Formulário ------------------
    st.subheader("Adicionar / Editar Local")
    nome = st.text_input("Nome do Local", value="" if st.session_state.edit_local_id is None else st.session_state.edit_nome)
    cidade_selecionada = st.selectbox("Cidade", [c['name'] for c in get_cities()],
                                      index=0 if st.session_state.edit_local_id is None else st.session_state.edit_cidade_index)
    latitude = st.number_input("Latitude", value=st.session_state.lat, format="%.6f")
    longitude = st.number_input("Longitude", value=st.session_state.lon, format="%.6f")
    descricao = st.text_area("Descrição", value="" if st.session_state.edit_local_id is None else st.session_state.edit_descricao)

    if st.button("Salvar Local"):
        if nome and cidade_selecionada and latitude != 0.0 and longitude != 0.0:
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
        else:
            st.warning("Preencha todos os campos obrigatórios.")

    st.markdown("---")
    st.subheader("Locais Cadastrados")

    # ------------------ Lista de locais ------------------
    locais = LocalService().get_all_places()
    for l in locais:
        col1, col2, col3 = st.columns([4, 1, 1])
        col1.write(f"{l['nome_local']} — {l['cidade']} (Lat: {l['coordenadas']['latitude']}, Lon: {l['coordenadas']['longitude']})")
        if col2.button("✏️", key=f"edit_{l['_id']}"):
            st.session_state.edit_local_id = l["_id"]
            st.session_state.edit_nome = l["nome_local"]
            st.session_state.edit_cidade_index = [c['name'] for c in get_cities()].index(l["cidade"])
            st.session_state.edit_descricao = l.get("descricao", "")
            st.session_state.lat = l["coordenadas"]["latitude"]
            st.session_state.lon = l["coordenadas"]["longitude"]
        if col3.button("🗑️", key=f"delete_{l['_id']}"):
            collection = get_collection()
            collection.delete_one({"_id": l["_id"]})
            st.rerun()
