# Befehlsabfolge im Terminal bei Entwickling und Einrichtung des Mockup Data Pollers
## Grundeinrichtung Raspberry Pi 5
sudo raspi-config
	- i2c enable
	- full filesystem usable

sudo apt update
sudo apt upgrade
sudo autoremove

## Add Docker's official GPG key:
sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

## Add the repository to Apt sources:
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/debian
Suites: $(. /etc/os-release && echo "$VERSION_CODENAME")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF

sudo apt update

## Installation von Docker
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

## Installation der Rust-Lang Toolchain
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

## Reboot um den gesamten Speicherplatz verfügbar zu machen
sudo reboot

## docker Befehl ohne sudo für admin zugänglich machen
sudo usermod -aG docker admin

## Fernzugriff auf Raspi hergestellen
rpi-connect signin

## Hinzufügen von Wlan Netzwerken um die Funktion und Zugriff auf den Pi in der Schule zu gewährleisten
sudo nmtui

# Ausgabe von Git Log online vor der Bearbeitung der Dokumentation (Arbeitsschritte von neu nach alt)
* 930ba28 update .gitignore to include rust build files
* 601bfec add .gitignore file ignoring container data directories
* f59f62a correct container bootorder in compose file
* 8d2b63d change data console output to writing to mariadb
* 0838da5 add dependencies for rust-poller
* 8105cb1 init empty rust project for alternative poller
* 69808f9 rename src/python to src/python-poller
* 3814b3f move python container resources into subdirectory
* ac65c25 add python app for polling data from bmp280
* 0b0f3d0 add compose.yaml for settig up project as docker environment
* 8c57b8c add INSTALL.md with all steps to setup raspi
* 601bfec add .gitignore file ignoring container data directories
* f59f62a correct container bootorder in compose file
* 8d2b63d change data console output to writing to mariadb
* 0838da5 add dependencies for rust-poller
* 8105cb1 init empty rust project for alternative poller
* 69808f9 rename src/python to src/python-poller
* 3814b3f move python container resources into subdirectory
* ac65c25 add python app for polling data from bmp280
* 0b0f3d0 add compose.yaml for settig up project as docker environment
* 8c57b8c add INSTALL.md with all steps to setup raspi
