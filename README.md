# Smart-temperature-monitoring

connect to the Raspberry pi through WSL from Windows:
ssh -i ~/.ssh/pi-key pi@192.168.0.25
How to check the data set
![image](https://github.com/user-attachments/assets/d248cf47-d074-4323-890a-05eb03d71a75)
# Raspberry Pi Temperature Monitoring with Ansible and Docker

This project provisions a Raspberry Pi (using Ansible in a Docker container) to monitor indoor and outdoor temperature. It installs and configures a stack of services for data collection and visualization, including InfluxDB and Grafana. 

Tested on **Raspberry Pi OS Lite (64-bit)** with a **Raspberry Pi 4 Model B**.

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

## Requirements
- **Raspberry Pi 3 Model B+ or 4 Model B** (Gigabit-capable recommended)
- **Docker** >= v20.10.17
- **GNU Make** >= 4.3
- **Raspberry Pi OS Lite (64-bit)** (recommended)

---

## Services Installed
1. **InfluxDB v2.4.0** – Time-series database to store sensor data  
2. **Grafana v9.2.0** – Visualization and dashboards  
3. **Cron job** – Automates the speedtest script execution  
4. **Speedtest CLI v1.2.0** – Tests internet speed  
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
   If your operating system does not provide it by default, install GNU Make >= 4.3.

3. **Generate an SSH Key**  
   Generate an SSH key pair to securely connect to the Raspberry Pi:  
   ```bash
   ssh-keygen
