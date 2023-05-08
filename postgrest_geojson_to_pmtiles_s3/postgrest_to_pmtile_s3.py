import os
import requests
import json
import subprocess

# Load the layer list from the ConfigMap
layers = json.loads(os.environ.get('LAYER_NAMES'))['layers']
print(layers)
s3URL = os.environ.get('S3_URL')
s3BucketName = os.environ.get('S3_BUCKET')
try:
    for layer in layers:
        layerName = layer['name']
        pgURL = os.environ.get('PGRST_URL')
        fullURL = pgURL + '/' + layerName

        response = None
        first = None
        data = None
        try:
            response = requests.get(fullURL)
            with open('riso.json', 'r') as file:
                data = file.read()
        except Exception as e:
            print('error fetching layer data')
            print(e)
            break 


        try: 
            #first = json.loads(response.text)[0]['featurecollection']
            ajson = (json.loads(data))
            #first = json.loads(data)[0]['rows'][0]
            first = ajson
        except Exception as e: 
            print('error parsing response json from server')
            print(e)
            break 


        try:
            with open('tippecanoe_input.json', 'w') as f:
                f.write(json.dumps(first))
        except Exception as e: 
                print(e)
                break 

        try:
            #subprocess.run(['ls', '~/.aws'], check=True)
            subprocess.run(['aws', 'configure', 'list-profiles'], check=True)
            subprocess.run(['rm', '-rf', 'tiles.pmtiles'], check=True)
            subprocess.run(['tippecanoe', '-zg', '--projection=EPSG:4326', 'tippecanoe_input.json', '--output=tiles.pmtiles', '--no-tile-compression'  ], check=True)
            #aws s3 --endpoint-url https://nrs.objectstore.gov.bc.ca/ cp p s3://seeds --profile=inv --acl public-read 

            subprocess.run(['aws', 's3', '--endpoint-url', f'{s3URL}', 'rm', f's3://{s3BucketName}/{layerName}.pmtiles', '--profile=inv' ], check=True)
            subprocess.run(['aws', 's3', '--endpoint-url', f'{s3URL}', 'cp', 'tiles.pmtiles', f's3://{s3BucketName}/{layerName}.pmtiles', '--profile=inv', '--acl', 'public-read' ], check=True)
        except Exception as e: 
           print('error creating pm tiles')
           print(e)
           break 



        #//subprocess.run(['aws', 's3', 'cp', 'tiles.mbtiles', os.environ.get('S3_URI', '')], check=True)



except (RuntimeError, TypeError, NameError)  as e:
    print(e)