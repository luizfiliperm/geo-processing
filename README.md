# Projeto de Persistência Poliglota com Geo-Processamento 🗺️

Aplicação prática utilizando **persistência poliglota** (SQLite + MongoDB) e recursos de **geoprocessamento** em Python com Streamlit, rodando dentro de containers Docker.

## Objetivo
Desenvolver uma aplicação para armazenar e consultar dados em diferentes contextos, utilizando SQLite para dados tabulares e MongoDB para documentos JSON com coordenadas geográficas, além de visualizar e consultar locais em um mapa interativo.

## Tecnologias e Bibliotecas
- Python 3.10+
- [Streamlit](https://streamlit.io/) – Interface interativa
- [SQLite3](https://www.sqlite.org/) – Banco relacional
- [PyMongo](https://pymongo.readthedocs.io/) – Integração com MongoDB
- [Geopy](https://geopy.readthedocs.io/) – Cálculo de distâncias
- [Folium](https://python-visualization.github.io/folium/) – Visualização no mapa
- [Pandas](https://pandas.pydata.org/) – Manipulação de dados
- Docker & Docker Compose – Containers para MongoDB e Streamlit

## Funcionalidades
- Cadastro de locais com nome, cidade, coordenadas e descrição (MongoDB).
- Cadastro de cidades/estados em tabela (SQLite).
- Consulta integrada: exibir locais do MongoDB relacionados a uma cidade do SQLite.
- Proximidade geográfica: dado um ponto (latitude/longitude), listar os locais próximos.
- Visualização de locais no mapa dentro do Streamlit.
- Interface interativa para inserir e editar dados, selecionar cidades e consultar locais próximos.

## Estrutura do projeto
```
.
├── docker-compose.yml         # Configuração dos containers (MongoDB + Streamlit)
├── Dockerfile                 # Build da aplicação Python
├── migrations/                # Scripts SQL para criação das tabelas no SQLite
│   ├── 01-create_country.sql
│   └── 02-create_city.sql
├── requirements.txt           # Dependências do projeto
├── src/                       # Código-fonte principal
│   ├── app.py                 # Ponto de entrada da aplicação Streamlit
│   ├── db_mongo.py            # Conexão e operações no MongoDB
│   ├── db_sqlite.py           # Conexão e operações no SQLite
│   ├── domains/               # Definição das entidades do sistema
│   │   ├── city.py
│   │   ├── country.py
│   │   └── state_enum.py
│   ├── geoprocessing.py       # Funções para cálculo de distâncias e operações geográficas
│   ├── services/              # Camada de regras de negócio
│   │   ├── city_service.py
│   │   ├── country_service.py
│   │   └── place_service.py
│   └── ui/                    # Interface Streamlit (telas e formulários)
│       ├── city_ui.py
│       ├── country_ui.py
│       ├── form_place_ui.py
│       ├── place_query_ui.py
│       └── render_place_page.py

```

## Executando via Docker

1. Certifique-se de ter **Docker** e **Docker Compose** instalados.  
2. Clone o repositório:
```bash
git clone https://github.com/luizfiliperm/geo-processing.git
cd geo-processing
```
3.Suba os containers:
```bash
docker-compose build;
docker-compose up;
```
4. Acesse a aplicação Streamlit pelo navegador:
 ```
 http://localhost:8501
 ```
## Exemplos de uso
- Inserir uma novo pais, cidade ou local.
- Consultar locais próximos a uma coordenada fornecida.
- Visualizar locais cadastrados no mapa interativo.

## Demonstração

[https://github.com/luizfiliperm/geo-processing/issues/5#issue-3459036484](https://github.com/user-attachments/assets/e1a6fcf3-a9da-46a1-ad63-d2ecc8e1cf6c)

## Professor
Ricardo Roberto de Lima
