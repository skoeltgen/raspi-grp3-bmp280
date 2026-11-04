# Installation
git clone https://github.com/skoeltgen/raspi-grp3-bmp280.git

cd temp-sensor/src/python-poller

sudo docker build --tag python_poller .

cd ../..

sudo docker compose up -d
