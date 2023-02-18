FROM python:3.9
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

run git clone https://github.com/felt/tippecanoe.git && cd tippecanoe && make -j && make install

CMD [ "python", "./postgrest_to_pmtile_s3.py" ]