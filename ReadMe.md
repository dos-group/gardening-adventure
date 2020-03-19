
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
This project provides an infrastructure to implement a self sustaining smart garden. It uses state-of-the-art technologies to implement a variety of useful tools to monitor, alert and explore on the basis of the data.
The core of our work is the implementation of a greenhouse which provides sensors and actuators controlled via cloud systems to provide an optimal environment for plants.

In picture 1 we can see in the general overview the idea to connect multiple greenhouses via a wifi network mesh to a Cloud service. Whereby particular greenhouses can serves as a gateway and are directly connected to the cloud.
![Overview](./documentation/diagrams/concept_overview_1.png)

The greenhouses themselves contain a variety of sensors and actuators, as shown in Figure 2. These sensors and actuators are connected via the GPIO connectors to an Raspberry pi.  The Raspberry pi gathers the sensor data and distributes this data via the above mentioned mesh network. The Pi also receives instructions for the connected actuators and executes them.
![Overview](./documentation/diagrams/concept_overview_3.png)
Figure 3 gives an overview about the Software implementation. In the lower part we see Multiple Pi's which implement the mesh network via [B.A.T.M.A.N](https://www.open-mesh.org/projects/open-mesh/wiki). B.A.T.M.A.N. (better approach to mobile ad-hoc networking) is a routing protocol for multi-hop ad-hoc mesh networks. The sensor & actuator logic is implemented via Python and containerized in [Docker](https://www.docker.com/). Each Raspberry is a Worker Node in a [K3s](https://k3s.io/) cluster.  K3s is a lightweight Kubernetes built for IoT & Edge computing. It perfect to for running on something as small as a Raspberry Pi.  
The sensor communication is realized via [MQTT](http://mqtt.org/). In particular we use [Phao mqtt](https://www.eclipse.org/paho/) for pyhton on the Pi side and a Mosquitto MQTT Broker on the cloud side. 
![Overview](./documentation/diagrams/concept_overview_2.png)
The cloud environment  consists of four services. A [Mosquitto](https://mosquitto.org/man/mqtt-7.html) MQTT broker for the communication with the greenhouse instances. [Telegraf](https://www.influxdata.com/time-series-platform/telegraf/) which subscribes to the published topics by the greenhouse sensors and  saves the data in an [influxdb](https://www.influxdata.com/) database. And lastly [Grafana](https://grafana.com/) which is used for data visualization and alerting.   
## Goal

# Prerequisites & Components
For the creation of the project we used a desktop computer as cloud environment(Master node) and raspberry pi's as worker nodes

### Components listed per greenhouse.

| Component                 | Description                   | 
| ------------------------- | ----------------------------- |
| Raspberry Pi 3B / 4       | Content Cell                  | 
| MicroSD Card 32GB         | Content Cell                  |
| DHT22 Sensor              | Temperature & Humidity Sensor |
| Water Level Sensor        | Analog Water Level Sensor     |
| Soil Moisture Sensor      | Analog Soil Moisture Sensor   |
| LDR                       | Light Dependent Resistor      |
| MCP3008                   | 8 Channel 10-bit ADC          |
| Breadboard                | -                             |
| Male to Male Connectors   | -                             |
| Male to Female Connectors | -                             | 
| 5v Power Supply           | 2.5A Power Supply recommended | 
| 5v Waterpump              | Water pump                    |
| RGB LED                   | NeoPixel Ring - 12 x RGB LED  |
| Jumper-Cabel              | 5v power supply for LED       | 

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

## Setting up Kubernetes


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
## Setting up the Cloud Environment

# Connecting Sensors

![Wiring Diagram](./documentation/diagrams/wiring&#32;diagram/Wiring&#32;Diagram_bb.png)
