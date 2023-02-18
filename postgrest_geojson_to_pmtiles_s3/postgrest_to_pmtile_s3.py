import os
import requests
import json
import subprocess

# Load the layer list from the ConfigMap
layers = json.loads(os.environ.get('LAYER_NAMES'))['layers']
print(layers)
try:
    for layer in layers:
        layerName = layer['name']
        pgURL = os.environ.get('PGRST_URL')
        fullURL = pgURL + '/' + layerName
        response = requests.get(fullURL)

        with open('tippecanoe_input.json', 'w') as f:
            f.write(response.text)

        subprocess.run(['tippecanoe', '--output=tiles.mbtiles', '--input=tippecanoe_input.json'], check=True)

        #//subprocess.run(['aws', 's3', 'cp', 'tiles.mbtiles', os.environ.get('S3_URI', '')], check=True)



except (RuntimeError, TypeError, NameError)  as e:
    print(e)