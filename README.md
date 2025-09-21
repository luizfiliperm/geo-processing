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

## Executando via Docker

1. Certifique-se de ter **Docker** e **Docker Compose** instalados.  
2. Clone o repositório:
```bash
git clone https://github.com/luizfiliperm/geo-processing.git
cd geo-processing
```
3.Suba os containers:
```
docker-compose up --build
```
4. Acesse a aplicação Streamlit pelo navegador:
 ```
 http://localhost:8501
 ```
## Exemplos de uso
- Inserir uma novo pais, cidade ou local.
- Consultar locais próximos a uma coordenada fornecida.
- Visualizar locais cadastrados no mapa interativo.

## Professor
Ricardo Roberto de Lima
