from decouple import config
import psycopg2
import pandas as pd

def fetch_sorted_titles():
    connection = psycopg2.connect(
        host = config('DB_HOST'),
        dbname = config('DB_NAME'),
        port = config('DB_PORT'),
        user = config('DB_USER'),
        password = config('DB_PASSWORD')
    )

    query = """
        SELECT id, name
        FROM coreapi_product
        ORDER BY LOWER(name);
    """

    df = pd.read_sql(query, connection)
    connection.close()
    
    return df


