import os
import requests
import psycopg2
import subprocess
import json

# Load the layer list from the ConfigMap
layers = json.loads(os.environ.get('LAYER_NAMES'))['layers']

# Connect to the PostgreSQL server
conn = psycopg2.connect(os.environ.get('PGRST_DB_URI', ''))
cursor = conn.cursor()
limit = 1000

# Fetch the data from each WFS layer and store it in the PostgreSQL server
try:
    for layer in layers:
        layerName = layer['name']
        cursor.execute(f'CREATE TABLE IF NOT EXISTS {layerName} (id SERIAL PRIMARY KEY, featureCollection jsonb )')
        conn.commit()
        offset = 0
        features = []
        sortKey = layer['sortKey']
        while True:
            wfs_url = layer['url']
            fullURL = f'{wfs_url}&startIndex={offset}&count={limit}&sortby={sortKey}'
            response = requests.get(fullURL)
            data = response.json()
            cursor.execute(f"INSERT INTO {layerName} (featureCollection) VALUES (%s)", [json.dumps(data)])
            conn.commit()
            print('inserted data')
            if len(data['features']) < limit:
                break
            offset += limit
except (RuntimeError, TypeError, NameError)  as e:
    print(e)