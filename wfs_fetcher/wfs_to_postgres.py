import os
import requests
import psycopg2
import json

# Load the layer list from the ConfigMap
layers = json.loads(os.environ.get('LAYER_NAMES'))['layers']

# Connect to the PostgreSQL server
conn = psycopg2.connect(os.environ.get('PGRST_DB_URI', ''))
cursor = conn.cursor()
limit = 1000

try:
    cursor.execute('create role web_anon nologin')
    cursor.execute('grant usage on schema public to web_anon')
    conn.commit()
except(psycopg2.errors.DuplicateObject, RuntimeError, TypeError, NameError)  as e:
    print(e) 
    cursor.execute("ROLLBACK")

# Fetch the data from each WFS layer and store it in the PostgreSQL server
try:
    for layer in layers:
        #table setup
        layerName = layer['name']
        cursor.execute(f'CREATE TABLE IF NOT EXISTS {layerName} (id SERIAL PRIMARY KEY, featureCollection jsonb )')
        cursor.execute(f'truncate table {layerName};')
        conn.commit()


        #postgrest setup
        try:
            cursor.execute(f'grant select on public.{layerName} to web_anon;')
            conn.commit()
        except (psycopg2.errors.DuplicateObject, RuntimeError, TypeError, NameError)  as e:
            print(e)
            cursor.execute("ROLLBACK")

        offset = 0
        features = []
        sortKey = layer['sortKey']
        while True:
            wfs_url = layer['url']
            fullURL = f'{wfs_url}&startIndex={offset}&count={limit}&sortby={sortKey}&SRSNAME=EPSG:4326'
            print(fullURL)
            response = requests.get(fullURL)
            data = response.json()
            cursor.execute(f"INSERT INTO {layerName} (featureCollection) VALUES (%s)", [json.dumps(data)])
            print('inserted')
            conn.commit()
            break;
            if len(data['features']) < limit:
                break
            offset += limit
except (RuntimeError, TypeError, NameError)  as e:
    print(e)