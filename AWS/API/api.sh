#!/bin/bash -xe

apt update
apt upgrade -y
apt install python3-pip -y


REQUIREMENTS = "anyio==3.4.0
asgiref==3.4.1
certifi==2021.10.8
charset-normalizer==2.0.9
click==8.0.3
fastapi==0.70.0
h11==0.12.0
idna==3.3
pydantic==1.8.2
python-dotenv==0.19.2
requests==2.26.0
sniffio==1.2.0
starlette==0.16.0
typing_extensions==4.0.1
urllib3==1.26.7
uvicorn==0.16.0"

echo -n "$REQUIREMENTS" > $HOME/requirements.txt 
pip3 install -r $HOME/requirements.txt

apt install nginx

ELASTIC_IP = $(curl http://checkip.amazonaws.com)

NGINX_CONF = "server {    

        listen 80;

        listen 443 ssl;

        ssl on;

        ssl_certificate /etc/nginx/ssl/server.crt;    

        ssl_certificate_key /etc/nginx/ssl/server.key;
    
        server_name ${ELASTIC_IP};

        location / {

                proxy_pass http://127.0.0.1:8000;    

        }

}"

MAIN = "from fastapi import FastAPI
from presignedURL import presignedURL

app = FastAPI()

@app.get('/get/')
def signedURL(filename: str):
    return presignedURL(filename= filename, mode= 'get_object')



@app.get('/put/')
def signedURL(filename: str):
    return  presignedURL(filename= filename, mode= 'put_object')
"

PRESIGNED_URL='import logging
import boto3
from botocore.exceptions import ClientError

BUCKET_NAME = "handboll-ai-coach"
EXPIRATION = 3600

def decorator(func):
    def wrapper(*args, **kwargs):
        response = {}
        response["url"] = func(*args, **kwargs)
        response["filename"] = kwargs["filename"]
        response["mode"] = kwargs["mode"]
        response["expiration"] =  EXPIRATION
        response["bucket_name"] =  BUCKET_NAME
        return response
    return wrapper

@decorator
def presignedURL(filename: str, mode: str) -> str:
    """Generate a presigned URL to get/post an S3 object

    Parameters
    ----------
        filename: str
            Name of the file
        mode: str
            Type of operation (get_object or put_object)
    
    Returns
    -------
        presigned_URL: str
            Presigned url for AWS S3 bucket object
    """

    s3_client = boto3.client("s3")
    try:
        response = s3_client.generate_presigned_url(mode,
                                                    Params={"Bucket": BUCKET_NAME,
                                                            "Key": filename},
                                                    ExpiresIn=EXPIRATION)
    except ClientError as e:
        logging.error(e)
        return None

    return response
'


echo -n "$NGINX_CONF" > /etc/nginx/sites-enabled/api
echo -n "$MAIN" > ~/api/main.py
echo -n "$PRESIGNED_URL" > ~/api/presignedURL.py



apt-get install openssl

mkdir /etc/nginx/ssl

openssl req -batch -x509 -nodes -days 365 \-newkey rsa:2048 \-keyout /etc/nginx/ssl/server.key \-out /etc/nginx/ssl/server.crt


service nginx reload
python3 -m uvicorn main:app