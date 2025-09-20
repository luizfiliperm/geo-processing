import streamlit as st
from db_sqlite import get_connection
from db_mongo import get_collection

st.title("Projeto Persistência Poliglota 🚀")
st.subheader("Teste inicial de conexões")

try:
    conn_sqlite = get_connection()
    cursor = conn_sqlite.cursor()
    cursor.execute("SELECT 1")
    st.success(f"✅ Conexão com SQLite funcionando!")
except Exception as e:
    st.error(f"❌ Erro na conexão com SQLite: {e}")

try:
    collection = get_collection()
    collection.database.client.admin.command("ping")
    st.success(f"✅ Conexão com MongoDB funcionando! Collection: {collection.name}")
except Exception as e:
    st.error(f"❌ Erro na conexão com MongoDB: {e}")
