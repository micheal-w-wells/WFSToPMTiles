import os
import requests
import json

# Load the layer list from the ConfigMap
layers = json.loads(os.environ.get('LAYER_NAMES'))['layers']
print(layers)
try:
    for layer in layers:
        #table setup
        layerName = layer['name']

        pgURL = os.environ.get('PGRST_URL')
        print(pgURL)
        fullURL = pgURL + '/' + layer['name']
        response = requests.post(os.environ.get('PGRST_URL') + '/' + layer['name'])
        print(response.json())

except (RuntimeError, TypeError, NameError)  as e:
    print(e)