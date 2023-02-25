FROM --platform=linux/amd64 python:3.9
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

run git clone https://github.com/felt/tippecanoe.git && cd tippecanoe && make -j && make install
RUN	curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN	unzip awscliv2.zip && ./aws/install

COPY postgrest_to_pmtile_s3.py .
copy ./credentials ./credentials
copy ./config ./config
env AWS_CONFIG_FILE=./config
env AWS_SHARED_CREDENTIALS_FILE=./credentials

CMD [ "python", "./postgrest_to_pmtile_s3.py" ]