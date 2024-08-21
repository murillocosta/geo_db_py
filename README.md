# GeoDB Py

GeoDB Py é um projeto de geoprocessamento que utiliza Python para interagir com um banco de dados PostgreSQL/PostGIS. O objetivo é fornecer ferramentas para ler e postar dados geoespaciais entre arquivos shapefile e uma base de dados PostGIS, além de realizar operações básicas de filtragem e transformação de dados.

## Descrição

Este repositório contém scripts Python para:
- Conectar-se a um banco de dados PostgreSQL/PostGIS.
- Ler arquivos shapefile e postar dados no banco de dados PostGIS.
- Filtrar e manipular dados geoespaciais.

## Funcionalidades

- **Conexão com PostgreSQL:** Estabelece uma conexão com o banco de dados PostgreSQL usando SQLAlchemy.
- **Postar Shapefiles:** Lê arquivos shapefile e posta os dados em uma tabela do banco de dados PostGIS.
- **Filtrar Dados:** Filtra dados com base em critérios específicos e lê dados filtrados de uma tabela PostGIS.

## Instalação

1. Clone o repositório:

    ```bash
    git clone https://github.com/murillocosta/geo_db_py.git
    cd geo_db_py
    ```

2. Crie um ambiente virtual e ative-o:

    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
    ```

3. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

## Uso

1. **Conectar ao Banco de Dados:**

    Atualize o arquivo `connection_params` com suas credenciais do PostgreSQL e execute a função `db_connect`.

2. **Postar um Shapefile:**

    Atualize o arquivo `file_params` com o caminho do shapefile e o nome da tabela desejada. Em seguida, execute a função `post_shp_to_postgis`.

3. **Ler Dados do Banco de Dados:**

    Execute a função `read_geodataframe_to_postgis` para ler dados de uma tabela no PostGIS usando um código de registro específico.

## Exemplo de Código

```python
# Conectar ao banco de dados
db_connection = db_connect(ip_host='localhost', db_name='mba_geo', db_port='5432', user='postgres', password='123456')

# Postar shapefile
post_shp_to_postgis(file_path='path/to/shapefile.shp', table_name='my_table', crs_epsg=4674, db_connection=db_connection)

# Ler dados
gdf = read_geodataframe_to_postgis(registration='your_registration_code', table_name='my_table', db_connection=db_connection)
print(gdf)
