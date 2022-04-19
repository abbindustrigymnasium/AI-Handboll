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

NGINX_CONF = "server {    

        listen 80;

        listen 443 ssl;

        ssl on;

        ssl_certificate /etc/nginx/ssl/server.crt;    

        ssl_certificate_key /etc/nginx/ssl/server.key;
    
        server_name ELASTIC_IP;

        location / {

                proxy_pass http://127.0.0.1:8000;    

        }

}"

echo -n "$NGINX_CONF" > /etc/nginx/sites-enabled/api



apt-get install openssl

mkdir /etc/nginx/ssl

sudo openssl req -batch -x509 -nodes -days 365 \-newkey rsa:2048 \-keyout /etc/nginx/ssl/server.key \-out /etc/nginx/ssl/server.crt


service nginx reload
python3 -m uvicorn main:app