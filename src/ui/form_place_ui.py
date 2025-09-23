import streamlit as st
import folium
from services.Place_service import PlaceService
from streamlit_folium import st_folium
from db_mongo import get_collection
from db_sqlite import get_cities

def render_local_page():
    st.header("📍 Gerenciar Locais")

    # ------------------ Inicialização do session_state ------------------
    if "lat" not in st.session_state:
        st.session_state.lat = -7.11532
    if "lon" not in st.session_state:
        st.session_state.lon = -34.861
    if "edit_place_id" not in st.session_state:
        st.session_state.edit_place_id = None
    if "edit_name" not in st.session_state:
        st.session_state.edit_name = ""
    if "edit_city_index" not in st.session_state:
        st.session_state.edit_city_index = 0
    if "edit_description" not in st.session_state:
        st.session_state.edit_description = ""

    # ------------------ Mapa ------------------
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
    name = st.text_input(
        "Nome do Local",
        value="" if st.session_state.edit_place_id is None else st.session_state.edit_name
    )
    cidades = [c['name'] for c in get_cities()]
    selected_city = st.selectbox(
        "Cidade",
        cidades,
        index=0 if st.session_state.edit_place_id is None else st.session_state.edit_city_index
    )
    latitude = st.number_input("Latitude", value=st.session_state.lat, format="%.6f")
    longitude = st.number_input("Longitude", value=st.session_state.lon, format="%.6f")
    description = st.text_area(
        "Descrição",
        value="" if st.session_state.edit_place_id is None else st.session_state.edit_description
    )

    if st.button("Salvar Local"):
        if name and selected_city and latitude != 0.0 and longitude != 0.0:
            collection = get_collection()
            if st.session_state.edit_place_id:
                
                collection.update_one(
                    {"_id": st.session_state.edit_place_id},
                    {"$set": {
                        "place_name": name,
                        "city": selected_city,
                        "coordinates": {"latitude": latitude, "longitude": longitude},
                        "description": description
                    }}
                )
                st.success(f"Local '{name}' atualizado com sucesso!")
                st.session_state.edit_place_id = None
            else:
                
                collection.insert_one({
                    "place_name": name,
                    "city": selected_city,
                    "coordinates": {"latitude": latitude, "longitude": longitude},
                    "description": description
                })
                st.success(f"Local '{name}' adicionado com sucesso!")
        else:
            st.warning("Preencha todos os campos obrigatórios.")

    st.markdown("---")
    st.subheader("Locais Cadastrados")

    # ------------------ Lista de locais ------------------
    places = PlaceService().get_all_places()
    for p in places:
        nome = p.get("place_name") or "Sem nome"
        cidade = p.get("city") or "Sem cidade"
        coords = p.get("coordinates") or {"latitude":0, "longitude":0}

        col1, col2, col3 = st.columns([4, 1, 1])
        col1.write(f"{nome} — {cidade} (Lat: {coords['latitude']}, Lon: {coords['longitude']})")

        if col2.button("✏️", key=f"edit_{p['_id']}"):
            st.session_state.edit_place_id = p["_id"]
            st.session_state.edit_name = nome
            st.session_state.edit_city_index = cidades.index(cidade) if cidade in cidades else 0
            st.session_state.edit_description = p.get("description", "")
            st.session_state.lat = coords['latitude']
            st.session_state.lon = coords['longitude']

        if col3.button("🗑️", key=f"delete_{p['_id']}"):
            PlaceService().delete_place(p["_id"])
            st.rerun()
