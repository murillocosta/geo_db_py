from sqlalchemy import create_engine
import geopandas as gpd

# Params of connection
connection_params = {
    'ip_host': 'localhost',
    'db_name': 'mba_geo',
    'db_port': '5432',
    'user': 'postgres',
    'password': '123456'
}

# File Params
file_params = {
    'file_path': '.\\AREA_IMOVEL\\AREA_IMOVEL_1.shp',
    'table_name': 'area_imovel',
    'crs_epsg': 4674,
}


def db_connect(ip_host: str, db_name: str, db_port: str, user: str, password: str):
    """
    Establishes a connection to a PostgreSQL database using SQLAlchemy.

    Returns:
        db_connection: SQLAlchemy engine object if the connection is successful.
        bool: Returns `False` if an error occurs during the connection attempt.
    """
    try:
        db_connection = create_engine(
            f"postgresql://{user}:{password}@{ip_host}/{db_name}")

        # Test connection
        connection = db_connection.connect()
        connection.close()

        print(f"{user.capitalize()} connected to database '{
              db_name}' on port {db_port}.")
        return db_connection

    except Exception as err:
        print(f"Error connecting to database. !! ERROR: {err.upper()} !!")
        return False


def post_shp_to_postgis(file_path: str, table_name: str, crs_epsg: int, db_connection: create_engine) -> gpd.GeoDataFrame:
    """
    Reads a shapefile, reprojects it, and posts it to a PostGIS database.

    Args:
        file_path (str): Path to the shapefile.
        table_name (str): Name of the table in PostGIS.
        crs_epsg (int): EPSG code for coordinate reference system.
        db_connection (create_engine): Database connection object.

    Returns:
        gpd.GeoDataFrame: The GeoDataFrame that was posted to PostGIS.
    """
    try:
        gdf = gpd.read_file(file_path)

        # Filter for rows where 'municipio' is 'Itacaré'
        # gdf = gdf[gdf['municipio'] == 'Itacare']

        gdf.columns = gdf.columns.str.lower()

        # Reproject the GeoDataFrame
        gdf = gdf.to_crs(epsg=crs_epsg)

        # Post the GeoDataFrame to PostGIS
        gdf.to_postgis(name=table_name, con=db_connection, if_exists='replace')

        print(f"Shapefile '{file_path}' successfully posted to table '{
              table_name}'.")
        return gdf

    except Exception as err:
        print(f"Error posting shapefile to PostGIS. !! ERROR: {
              err.upper()} !!")
        return None


def read_geodataframe_to_postgis(registration: str, table_name: str, db_connection: create_engine) -> gpd.GeoDataFrame:
    """
    Reads data from a PostGIS table based on a specific registration code and returns it as a GeoDataFrame.

    Args:
        registration (str): The registration code to filter the data by (e.g., a property code).
        table_name (str): The name of the table in PostGIS to query.
        db_connection (create_engine): SQLAlchemy database connection object.

    Returns:
        gpd.GeoDataFrame: A GeoDataFrame containing the filtered data from the PostGIS table.
    """
    # SQL query with a placeholder for the registration code
    sql = f"SELECT * FROM {table_name} WHERE cod_imovel = %s"
    print('SQL:', sql)

    # Read data from PostGIS using the query and the specified geometry column
    gdf = gpd.read_postgis(sql, db_connection, params=(
        registration,), geom_col='geometry')

    return gdf


# Functions calls
db_connection = db_connect(**connection_params)

if db_connection:
    post_shp_to_postgis(**file_params, db_connection=db_connection)

    # try:
    #     print(read_geodataframe_to_postgis(
    #         'BA-2914901-C70164ED10D548B3B38B8F743253FC11', 'area_imovel', db_connection))
        
    #     print('GDF reading done!')
    # except Exception as err:
    #     print(err)
