---
creationDate: 2026-09-23

tags:
  - schule

lastEditDate: 2026-11-04
---

# Doku

Gruppe 3: Sven Költgen, Moritz Valkysers

## Festlegung Systemumgebung und Projektkontext

- **OS**: PI OS Light 64 bit
  - Warum:
    -> leichtgewichtig und ressourcenschohnend
    -> keine Graphische Oberfläche nötig, das Arbeit via ssh - passt zu der gegebenen Hardware (Raspberry PI)
- **Systemsprache**: Deutsch
  - für Tastatus-Layout und Zeit
- **Accountdaten**
  - user:admin
  - pwd:admin
- **Zugriffsmöglichkeiten**
  - ssh, wenn in gleichem Netzwerk
  - Pi Connect (da das Netzwerk IT-Lab_Schueler P2P nicht zulässt)

---

## Installation und Einrichtung

### Vorraussetzungen

#### System

1. ein Raspberry PI mit Zubehör (Netzteil, SD-Karte, usw.)
2. mindestent 8 gb Speicherplatz für Container und Daten + X gb für PI OS
3. den Messsensor (z.B. Bosch BMP-280)

#### Software

1. git
2. Docker + Docker Compose + Docker Build
3. [lgpio Dokumentation](https://rpi-lgpio.readthedocs.io/en/latest/api.html)

#### Python

1. `mariadb`
2. `bmp280`
   - Keine API von Bosch gefunden (für den Sensore), daher das Pip-Package `bmp280-python` für das auslesen der Daten benutzt.

---

### Installation

Zum weiterem Informieren:

> **Offizielle Doku RasPi**: [https://www.raspberrypi.com/documentation/computers/getting-started.html](https://www.raspberrypi.com/documentation/computers/getting-started.html)<br>
> **Offizielle Doku BPM280** [https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmp280-ds001.pdf](https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmp280-ds001.pdf)

#### Grundlage

##### Vorgehen im PI Imager

1. Gerät auswählen
2. OS auswählen
3. SD-Karte zum schreiben auswählen
4. Hostnamen vergeben (raspi-grp3)
5. Zeitzone und Keyboardlayout setzen
6. Nutzer (admin) erstellen mit Passwort und Namen
7. "enable SSH" mit Passwort Authentication
8. Pi Connect aktivieren (da das Netzwerk P2P nicht zulässt)
9. dann Wirte image

##### WLAN Verbindung einrichten

Da wir eine **Netzwerkverbindung via Banutzername und Passwort** herstellen wollen, muss dies noch direkt im _Image_ konfiguriert werden, da dies nicht über den _PI Imager_ eingerichtet werden kann.

1. Terminal öffnen
2. in gemountetes SK-Karten verzeichnis navigieren
3. dort dann `/etc/NetworkManager/systemconnection/`
   - dort können Einträge angelegt werden, welche Anagaben über die verschiedenen Netzwerkverbinungen enthalten

**Hinweis**:
Da die einrichtung direkt am Gerät in der Schule nicht funktioniert hat in anderem Netzwerk eingerichtet. Deswegen in **P2P** `enabled network`:

1. login auf Pi
2. sudo nmtui
3. wlan auswählen
4. new (connection)
5. angaben nach vorgabe der Maske machen
6. wlan verbindung testen im Zielnetzwerk

##### Physischen Aufbau einrichten:

###### Verkabelung Sensor

1. Vcc zu pin1
2. gnd zu pin6
3. scl zu pin3
4. sda zu pin5

Weitere Informationen sind unter [https://pinout.xyz/](https://pinout.xyz/) zu finden.

##### Grundeinrichtung PI

###### Basics

1. `sudo raspi-config`
   1. `i2c enable`
   2. `full filesystem usable`
2. `sudo apt update && sudo apt upgrade`
3. `sudo autoremove`
4. `rpi-connect signin` -> Fernzugriff
5. `sudo apt install git`

###### Offizielle Docker GPG-Key hinzufügen

1. `sudo apt install ca-certificates curl`
2. `sudo install -m 0755 -d /etc/apt/keyrings`
3. `sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc`
4. `sudo chmod a+r /etc/apt/keyrings/docker.asc`
5. `sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin`
6. `sudo usermod -aG docker admin` -> Docker ohne `sudo`

Oder einfach der **[offiziellen Anleitung](https://docs.docker.com/engine/install/debian "https://docs.docker.com/engine/install/debian")** folgen.

---

#### GitHub Install

Diese Befehle müssen auf dem PI nacheinander ausgeführt werden:

1. `git clone https://github.com/skoeltgen/raspi-grp3-bmp280.git`
2. `cd temp-sensor/src/python-poller`
3. `sudo docker build --tag python_poller .`
4. `cd ../..`
5. `sudo docker compose up -d`

---

#### Händische Install

#### Grafana einrichten

Weitere Informationen sind unter [Grafana APT-Installation](https://grafana.com/docs/grafana/latest/setup-grafana/installation/debian/#install-from-apt-repository) zu finden.

#### I2C einrichten

1. `sudo raspi-config`
   -> 3 Interface Options
2. I5 I2C aktivieren
3. `sudo reboot`
4. `sudo apt isntall i2c-tools`

#### Grundeinrichtung PI

##### Repo zu APT-Sources hinzufügen

1. `sudo tee /etc/apt/sources.list.d/docker.sources`
   > EOFT
   > ypes: deb
   > URIs: https://download.docker.com/linux/debian
   > Suites: $(. /etc/os-release && echo "$VERSION_CODENAME")
   > Components: stable
   > Architectures: $(dpkg --print-architecture)
   > Signed-By: /etc/apt/keyrings/docker.asc
   > EOF
2. `sudo apt update`

##### Hinzufügen von Wlan Netzwerken

1. `sudo nmtui`

---

## Sonstiges

### Ausgabe von Git Log online vor der Bearbeitung der Dokumentation (Arbeitsschritte von neu nach alt)

- 930ba28 update .gitignore to include rust build files
- 601bfec add .gitignore file ignoring container data directories
- f59f62a correct container bootorder in compose file
- 8d2b63d change data console output to writing to mariadb
- 0838da5 add dependencies for rust-poller
- 8105cb1 init empty rust project for alternative poller
- 69808f9 rename src/python to src/python-poller
- 3814b3f move python container resources into subdirectory
- ac65c25 add python app for polling data from bmp280
- 0b0f3d0 add compose.yaml for settig up project as docker environment
- 8c57b8c add INSTALL.md with all steps to setup raspi
- 601bfec add .gitignore file ignoring container data directories
- f59f62a correct container bootorder in compose file
- 8d2b63d change data console output to writing to mariadb
- 0838da5 add dependencies for rust-poller
- 8105cb1 init empty rust project for alternative poller
- 69808f9 rename src/python to src/python-poller
- 3814b3f move python container resources into subdirectory
- ac65c25 add python app for polling data from bmp280
- 0b0f3d0 add compose.yaml for settig up project as docker environment
- 8c57b8c add INSTALL.md with all steps to setup raspi

### Rust Zukunft

#### Installation der Rust-Lang Toolchain

1. `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`
