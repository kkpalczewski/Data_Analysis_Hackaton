import psycopg2


def create_connection():
    conn_string = "host='85.194.245.31' dbname='locit_sample' user='sample_user' password='!TajemniczaTajemnica7'"
    return psycopg2.connect(conn_string)


def get_columns_from_neighbouring_grids_near_stations(column: str, stations, table_name: str, connection, grid_count):
    results = []
    cursor = connection.cursor()
    for station in stations:
        query = _build_query_grids(column, station, table_name, grid_count)
        cursor.execute(query)
        results.append(cursor.fetchall())

    return results


def _build_query_grids(column: str, station, table_name: str, grid_count):
    query_template = """SELECT 	#TABLE#.#COLUMN# 
                FROM	(
                    SELECT 
                      grid250.eurogrid_0250,
                      ST_Distance_sphere(ST_SetSRID(ST_MakePoint(#LONGITUDE#, #LATITUDE#),4674), ST_Centroid(ST_TRANSFORM(geometria92,4674) )) as dist
                    FROM 
                      locit_datasets.grid250
                    ORDER BY dist
                    LIMIT #GRIDS#
                ) as lista_id_gridow
                INNER JOIN locit_datasets.#TABLE#
                ON (lista_id_gridow.eurogrid_0250 = #TABLE#.eurogrid_0250)"""

    query_template = query_template.replace("#TABLE#", table_name)
    query_template = query_template.replace("#COLUMN#", column)
    query_template = query_template.replace("#LONGITUDE#", str(station[0]))
    query_template = query_template.replace("#LATITUDE#", str(station[1]))
    query_template = query_template.replace("#GRIDS#", str(grid_count))
    return query_template


def get_all_from_table(table_name: str, connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM locit_datasets." + table_name)
    return cursor.fetchall()


def get_columns_from_table(table_name, columns, connection):
    cursor = connection.cursor()
    columns_string = columns[0]
    if len(columns) > 1:
        for i in range(1, len(columns)):
            columns_string += ", " + columns[i]
    query = "SELECT " + columns_string + " FROM locit_datasets." + table_name
    cursor.execute(query)
    return cursor.fetchall()
