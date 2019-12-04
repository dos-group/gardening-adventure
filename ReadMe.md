Documentation for Urban Gardening

# Table of Contents

- [Table of Contents](#table-of-contents)
- [Introduction](#introduction)
  - [Goal](#goal)
- [Prerequisites & Components](#prerequisites--components)
  - [Components](#components)
  - [Initial Setup](#initial-setup)
- [Installation & Setup](#installation--setup)
  - [Preliminary setup](#preliminary-setup)
  - [setting up Kubernetes](#setting-up-kubernetes)
    - [Master node setup](#master-node-setup)
    - [worker node setup](#worker-node-setup)
  - [Setting B.A.T.M.A.N](#batman-setup)
    - [Gateway node setup](#gateway-node-setup)
    - [Mesh node setup](#mesh-node-setup)
  - [Testing Kubernetes](#testing-kubernetes)
- [Connecting Sensors](#connecting-sensors)

# Introduction
![Overview](./documentation/diagrams/concept_overview_1.png)
![Overview](./documentation/diagrams/technical_overview.png)
![Overview](./documentation/diagrams/concept_overview_2.png)
## Goal

# Prerequisites & Components

## Components

Components listed per greenhouse.

| Component                 | Description                   | Quantity |
| ------------------------- | ----------------------------- | :------: |
| Raspberry Pi 3B / 4B      | Content Cell                  |    4     |
| MicroSD Card 32GB         | Content Cell                  |    4     |
| DHT22 Sensor              | Temperature & Humidity Sensor |    4     |
| Water Level Sensor        | Analog Water Level Sensor     |    4     |
| Soil Moisture Sensor      | Analog Soil Moisture Sensor   |    4     |
| LDR                       | Light Dependent Resistor      |    4     |
| MCP3008                   | 8 Channel 10-bit ADC          |    4     |
| Breadboard                | -                             |    4     |
| Male to Male Connectors   | -                             |    30    |
| Male to Female Connectors | -                             |   100    |
| 5v Power Supply           | 2.5A Power Supply recommended |    4     |

## Initial Setup

- [Downloading Raspbian](https://www.raspberrypi.org/downloads/raspbian/)
- Writing the Raspbian Image to the SD Card
  - [Windows](https://www.raspberrypi.org/documentation/installation/installing-images/windows.md)
  - [Linux](https://www.raspberrypi.org/documentation/installation/installing-images/linux.md)
  - [MacOS](https://www.raspberrypi.org/documentation/installation/installing-images/mac.md)
  - [ChromeOS](https://www.raspberrypi.org/documentation/installation/installing-images/chromeos.md)

# Installation & Setup

## Preliminary setup

Start the RPi for the first time  
login with default username and password  
raspi-config

- change password
- add information for wireless access
- enable ssh
- update lists & upgrade packages
- restart system
- note down IP address
- disconnect monitor and ethernet, verify connectivity on Wireless and ssh access

## setting up Kubernetes

### Master node setup

### worker node setup

## Setting up B.A.T.M.A.N

A mesh network is created using B.A.T.M.A.N Adv. The resultant topology contains general nodes along with some nodes acting as gateways to connect to the server . The gateways nodes are connected to internet via ethernet and nodes are connected among each other on wlan using B.A.T.M.A.N Adv. The configuration for B.A.T.M.A.N Adv in your Pi are established through containers, by build corressponding images from the dockerfile listed under `batman` folder.

When you add a new node, make sure to modify the ip address listed in `bat0` file accordingly.

### Gateway node setup

Run the following commands from the directory that contains the dockerfile to build gateway image.

```bash
  docker build -t gateway-img .
```

Now, Run the container from the image

```bash
  docker run --network=host --privileged -d -it gateway-img /bin/bash gardening-adventure/batman/gateway/garden-mesh.sh
```

### Mesh node setup

Run the following commands from the directory that contains the dockerfile to build node image.

```bash
  docker build -t node-img .
```

Now, Run the container from the image

```bash
  docker run --network=host --privileged -d -it node-img /bin/bash gardening-adventure/batman/node/garden-mesh.sh
```

## Testing Kubernetes

# Connecting Sensors

![Wiring Diagram](./documentation/diagrams/wiring&#32;diagram/Wiring&#32;Diagram_bb.png)
