
# Raspberry Pi Temperature Monitoring with Ansible and Docker

This project provisions a Raspberry Pi (using Ansible in a Docker container) to monitor indoor and outdoor temperatures. It installs and configures a stack of services for data collection and visualization, including InfluxDB and Grafana. 

Tested on **Raspberry Pi OS Lite (64-bit)** with a **Raspberry Pi 4 Model B**.

![IMG_8869](https://github.com/user-attachments/assets/8e314bf3-e049-4ccb-b3b6-2e9d6d92c8e8)

---

## Table of Contents
- [Requirements](#requirements)
- [Services Installed](#services-installed)
- [Python Libraries](#python-libraries)
- [Setup](#setup)
- [Usage](#usage)
- [Customization Parameters](#customization-parameters)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## Hardware Requirements

- **Raspberry Pi 3 Model B+ or 4 Model B** (Gigabit-capable recommended)
- **DHT11 Temperature Sensor** (for monitoring indoor/outdoor temperature)
- **LCD Screen** (e.g., a 16x2 or 20x4 LCD with I2C or parallel interface) to display the temperature readings

---

## Software Requirements

- **Docker** >= v20.10.17  
- **GNU Make** >= 4.3  
- **Raspberry Pi OS Lite (64-bit)** (recommended)
  
---
## Services Installed
1. **InfluxDB v2.4.0** – Time-series database to store sensor data  
2. **Grafana v9.2.0** – Visualization and dashboards  
3. **Cron job** – Automates the speedtest script execution  
5. **influxdb-client-python v1.33.0** – Python client for InfluxDB  

---

## Python Libraries

- `board`
- `adafruit-circuitpython-dht`
- `RPLCD`
- `smbus2`
- `requests`
- `influxdb`
- `influxdb-client`
- `grafana-api`
- `toml`

These libraries enable interaction with sensors (e.g., DHT for temperature), LCD displays, and APIs for InfluxDB and Grafana.

---

## Setup

1. **Install Docker**  
   Make sure you have Docker >= v20.10.17 installed on the machine from which you will run the playbook.
2. **Install GNU Make**  
   - If your operating system does not provide it by default, install GNU Make >= 4.3.

3. **Generate an SSH Key**  
   - Generate an SSH key pair to securely connect to the Raspberry Pi:  
     ```bash
     ssh-keygen
     ```
   - Use a passphrase if you prefer additional security.

4. **Flash Raspberry Pi OS Lite (64-bit)**  
   - Use the Raspberry Pi Imager (or any other method) to write Raspberry Pi OS Lite (64-bit) to your SD card.  
   - Ensure **SSH** is enabled.  
   - Configure **Allow public-key authentication only** with your SSH key’s public key.

5. **Insert the SD Card & Power Up**  
   - Insert the prepared SD card into your Raspberry Pi.  
   - Connect the Pi to the same local network (LAN) as your workstation.  
   - Power on the Pi.

6. **Provision the Raspberry Pi**  
   - Run the following command from your workstation (the same machine on which Docker and Make are installed):
     ```bash
     make [HOST='...'] [SSH_USER='...'] [SSH_KEY='...'] [CRON='...']
     ```
   - By default:
     - `HOST=raspberrypi.local`  
     - `SSH_USER=pi`  
     - `SSH_KEY=~/.ssh/id_rsa`  
     - `CRON='*/30 * * * *'` (Runs speedtest every 30 minutes)
- example: make HOST='192.168.0.57' SSH_USER='pi' SSH_KEY='~/.ssh/pi-key' CRON='*/10 * * * * /home/pi/TempMonitoring/venv/bin/python /home/pi/TempMonitoring/TempMonitoring.py >> /home/pi/TempMonitoring/monitoring.log 2>&1' provision
---

## Usage

Once the provisioning is complete:

1. **Access InfluxDB**  
   - InfluxDB v2.4.0 is accessible on the default port `8086`.

2. **Access Grafana**  
   - Grafana v9.2.0 is accessible on the default port `3000`.  
   - Log in to Grafana to create or import dashboards for viewing temperature and speedtest metrics.

3. **Sensor Data Collection & LCD Display**  
   - Python scripts use the DHT11 to read indoor/outdoor temperature data.  
   - Temperature readings are displayed on the **LCD screen** in real time.  
   - Data is also sent to InfluxDB at regular intervals (as configured in the Ansible playbook).

---
## Customization Parameters

You can override the defaults when running `make`:
```bash
make HOST='my-pi.local' SSH_USER='myuser' SSH_KEY='/path/to/my_key' CRON='0 * * * *'


