



Documentation for Urban Gardening

# Table of Contents

- [Table of Contents](#table-of-contents)
- [Introduction](#introduction)
- [Prerequisites & Components](#prerequisites--components)
  - [Components listed per greenhouse](#components-listed-per-greenhouse)
- [Initial Setup](#initial-setup)
- [Installation & Setup](#installation--setup)
  - [Mesh Gateway Setup](#mesh-gateway-setup)
  - [Mesh Node Setup](#mesh-node-setup)
  - [Setting up the Cloud Environment](#setting-up-the-cloud-environment)
    - [Helm Deployment](#helm-deployment)
    - [Post Deployment Steps](#post-deployment-steps)
      - [Connecting Grafana with Influxdb](#connecting-grafana-with-influxdb)
      - [Grafana Charts](#grafana-charts)
      - [Grafana Alerts](#grafana-alerts)
        - [Create a Telegram Altert](#create-a-telegram-altert)
  - [Setting up the Greenhouse Environment](#setting-up-the-greenhouse-environment)
    - [Connecting Sensors](#connecting-sensors)
  - [Docker Sensor Images](#docker-sensor-images)
    - [Camera Configuration Options](#camera-configuration-options)
    - [Start Sensor and Actuators](#start-sensor-and-actuators)
- [Reference](#reference)

# Introduction

This project provides an infrastructure to implement a self sustaining smart garden. It uses state-of-the-art technologies to implement a variety of useful tools to monitor, alert and explore on the basis of the data.
The core of our work is the implementation of a greenhouse which provides sensors and actuators controlled via cloud systems to provide an optimal environment for plants.

In figure 1 we can see in the general overview the idea to connect multiple greenhouses via a wifi network mesh to a Cloud service. Whereby particular greenhouses can serves as a gateway and are directly connected to the cloud.
![Overview](./documentation/diagrams/concept_overview_1.png)

The greenhouses themselves contain a variety of sensors and actuators, as shown in figure 2. These sensors and actuators are connected via the GPIO connectors to an Raspberry pi.  The Raspberry pi gathers the sensor data and distributes this data via the above mentioned mesh network. The Pi also receives instructions for the connected actuators and executes them.
![Overview](./documentation/diagrams/concept_overview_3.png)

Figure 3 gives an overview about the Software implementation. In the lower part we see Multiple Pi's which implement the mesh network via [B.A.T.M.A.N](https://www.open-mesh.org/projects/open-mesh/wiki) (better approach to mobile ad-hoc networking) is a routing protocol for multi-hop ad-hoc mesh networks. The sensor & actuator logic is implemented via Python and containerized in [Docker](https://www.docker.com/). Each Raspberry is a Worker Node in a [K3s](https://k3s.io/) cluster.  K3s is a lightweight Kubernetes built for IoT & Edge computing. It perfect to for running on something as small as a Raspberry Pi.  
The sensor communication is realized via [MQTT](http://mqtt.org/). In particular we use [Paho mqtt](https://www.eclipse.org/paho/) for pyhton on the Pi side and a Mosquitto MQTT Broker on the cloud side. 
![Overview](./documentation/diagrams/concept_overview_2.png)
The cloud environment  consists of four services. A [Mosquitto](https://mosquitto.org/man/mqtt-7.html) MQTT broker for the communication with the greenhouse instances. [Telegraf](https://www.influxdata.com/time-series-platform/telegraf/) which subscribes to the published topics by the greenhouse sensors and  saves the data in an [influxdb](https://www.influxdata.com/) database. And lastly [Grafana](https://grafana.com/) which is used for data visualization and alerting.

# Prerequisites & Components

For the creation of the project we used a desktop computer as cloud environment(Master node) and raspberry pi's as worker nodes

## Components listed per greenhouse

| Component                 | Description                                                  |
| ------------------------- | ------------------------------------------------------------ |
| Raspberry Pi 3B / 4       | -                                                            |
| MicroSD Card 32GB         | -                                                            |
| DHT22 Sensor              | Temperature & Humidity Sensor                                |
| Water Level Sensor        | Analog Water Level Sensor                                    |
| Soil Moisture Sensor      | Analog Soil Moisture Sensor                                  |
| LDR                       | Light Dependent Resistor                                     |
| MCP3008                   | 8 Channel 10-bit ADC                                         |
| Breadboard                | 1 Piece                                                      |
| Male to Male Connectors   | 100 Pieces                                                   |
| Male to Female Connectors | 100 Pieces                                                   |
| 5v Power Supply           | Power supply for Raspberry Pi. 2.5A Power Supply recommended |
| 5v Waterpump              | Water pump (Not implemented)                                 |
| RGB LED                   | NeoPixel Ring - 12 x RGB LED                                 |
| Jumper-Cabel              | 5v power supply for LED                                      |

# Initial Setup

Custom raspbian OS creation is part of this repository which installs necessary packages and configurations for setting up `gateway` and `node` Pis respectively. The configuration files are listed under the folder `batman`. These files could further be modified according to the needs of the project. Also the image creation, requires Ubuntu/Debian OS.

To create an image:

1. Clone this git repository

2. Run the script build-batman-node.sh in the folder `garden-adventure`

  ```bash
        ./build-batman-node.sh -t [gateway|node] -n [hostname] -u [k3s_url] -k [k3s_token] -d [dns_ip]
  ```

Specify the required options for the above command(type, hostname, k3s url, k3s token). Mention your dns_ip when creating an image for `node`(eg: 8.8.8.8).

* The above command downloads the base image of raspbian STRETCH. This base image can be modified as per the needs by changing the base image url in the file `build-raspbian`.
* Further, the command creates two installation scripts under the root user as part of each image(gateway/node).
* Root user is created with the password `raspberry`. This can also be modified in the file `build-batman-node.sh`
* The image created, has only limited firmwares installed that are necessary for the project(`brcm` for wlan interface). Other firmwares could be installed from [here](https://github.com/RPi-Distro/firmware-nonfree). They should be copied at the time of image creation. Refer the script `build-batman-node.sh`.

# Installation & Setup

Using Raspberry Pi Imager, burn the created image onto a SD card. The created image could be found under the folder `images` after running above script.

- Writing the Raspbian Image to the SD Card
  - [Windows](https://www.raspberrypi.org/documentation/installation/installing-images/windows.md)
  - [Linux](https://www.raspberrypi.org/documentation/installation/installing-images/linux.md)
  - [MacOS](https://www.raspberrypi.org/documentation/installation/installing-images/mac.md)
  - [ChromeOS](https://www.raspberrypi.org/documentation/installation/installing-images/chromeos.md)

## Mesh Gateway Setup

First setup the gateway Pi by connecting it to ethernet and inserting the SD card that contains the raspbian OS for gateway and powering it on. The first boot steps will be performed and you can login with the details provided above. Under the root user following scripts can be found:

1. smart-garden-mesh.sh

2. k3s_installation.sh

Running the first script, brings up the B.A.T.M.A.N inteface for mesh network along with the Pi configured as a gateway. It starts a dhcp server for the inteface `bat0` and enables a custom service called `port-forwarding.service` that forwards packets across batman and ethernet interface.

Running the second script, installs K3s and adds the Pi as a worker to a K3s cluster. If the k3s master is not part of the same network as gateway and belongs to the public network, then k3s installation should be done via VPN. This is currently out of the scope of this repository. Refer [OpenVPN](https://openvpn.net/) or [Wiregaurd](https://www.wireguard.com/) for more information about setting up VPN.

## Mesh Node Setup

Setup the node by inserting the SD card that contains the raspbian OS for the node. The ethernet connection is not needed for the node setup. Also under the root user, the above mentioned scripts could be found.

1. First run smart-garden-mesh.sh to setup the B.A.T.M.A.N

2. Wait until the interface `bat0` gets an ip address from DHCP server within the range `172.27.0.100 - 172.27.0.200`. This may take a time of 20-30s.

3. Before running the K3s installation script, make sure the k3s master can direct packets to the node using `ping` command. If the packet loss is 100%, then you need to add necessary route in the k3s master using the command `ip`.

Eg: ``` ip route add 172.27.0.0/24 via 192.168.10.74 dev eth0 ```

## Setting up the Cloud Environment

This chapter describes the implementation of the Cloud services. In detail the installation of Grafana, Influxdb, Mosquitto MQTT Broker and Telegraf.

We use for all the cloud service installations [Helm](https://helm.sh) scripts. For the installation of Helm, please refer to the [documentation](https://helm.sh/docs/intro/quickstart/).

**Notice:** We used for all services the standard username: "admin" and password: "dspj2020"

### Helm Deployment

First add the Mosquitto Broker helom chart via: ` helm repo add smizy https://smizy.github.io/charts`
To start the services you can run the script in `gardening-adventure/cloud_garden/deployment/cloud_deployment.sh` This will start [Grafana](https://github.com/helm/charts/tree/master/stable/grafana), [Influxdb](https://github.com/helm/charts/tree/master/stable/influxdb), [Mosquitto MQTT Broker](https://github.com/smizy/charts/tree/master/mosquitto) and [Telegraf](https://github.com/helm/charts/tree/master/stable/telegraf) via helm. 

**Notice**: This will start the services without any node selection. For that edit the corresponding settings in the yaml files.  For adding a label to a node use the following command : `kubectl label nodes <nodename> <key>=<value> --overwrite`

### Post Deployment Steps
The Section gives examples for possible post deployment application of the services. This includes Database connections, charts and alerts.
#### Connecting Grafana with Influxdb

Login to the grafana UI. Use `kubectl get svc` to get the IP's and ports of all services.

1. Login to the Grafana Dashboard
2. Click the gear wheel icon on the left site and  select "Data Sources"
3. click "Add data source"
4. Choose Influxdb
5. Add the influxDB url `hhtp://<Influxdb IP>:8086`
6. Use `garden` as database
7. The default influxdb user is `admin` and password is `dspj2020`
8. Click `Save and Test`

#### Grafana Charts

After the datasource has been added the next step is to add the dashboard which displays the data from the datasource.

1. To create a Grafana dashboard click on `New dashboard`(Create -> New Dashboard -> Graph).
2. Click on Panel Title -> Edit. A new window with the graph will open up. Here we select the metric we would want to display in the graph. I will use the Temperature as an example.
3. Pick the data source that was defined earlier in the data source field. Tip: This should be influxdb datasource.
4. edit the query as follows -> in the `FROM` line, select the sensor name in the second dropdown. This will be the sensor that the graph will depict values from. In the `SELECT` line, pick the appropriate field, for example `temperature`. Pick the desired grouping time interval on line 3 and save the graph by clicking the save icon on the top right hand side.
5. Check the visibility of the data on the dashboard, the data should be available as a graph.
6. Repeat these steps for every data available from the sensors.

![Dashboard Query](./documentation/diagrams/grafana-query.png)

#### Grafana Alerts

We used [Grafana's Alerts](https://grafana.com/docs/grafana/latest/alerting/rules/) to receive [notifications](https://grafana.com/docs/grafana/latest/alerting/notifications/) when, for example, humidity drops below a certain level.
As an example we show here to configure an alert sent to telegram. For more options please have a look at the Grafana's alert documentation.

##### Create a Telegram Altert

1. Created a bot via @BotFather, and get an API token in telegram
2. Create new Chat Group in Telegram App, for example: “Super Dooper Alert Group” with people who need to be alerted.
3. Invite your bot to this group
4. Type at least one message in that group,  **this is very important**
5. Use cURL or just place this on any Browsers Address Bar: `https://api.telegram.org/bot<TOKEN>/getUpdates`
This should return an JSON object, you need to find key “chat” like this one:  
`"chat":{"id":-456343576,"title":"Super Dooper Alert Group","type":"group","all_members_are_administrators":true}`
6. Login to grafana
7. Click to the left Bell icon
8. Add notification channel
9. Select Telegram
10. Enable/disable settings you preger
11. Put Telegram API token to he fiel
12. Add chat ID (it starts with -, and that needs too)
13. Click Test notification
14. Save it.
15. Create a rule in the moister graph panel ![panel](https://grafana.com/static/img/docs/v4/drag_handles_gif.gif)
16. Go to dashboard
17. Select the desired Graph
18. Click Alarm icon
19. Click "Create Alert"

## Setting up the Greenhouse Environment

This chapter describes the installation of a new smart greenhouse.
The installation includes the hardware and the software configuration of the sensors/actuators and the Pi. 

### Connecting Sensors

Figure 4 shows the wiring of the sensors with the Raspberry Pi. Please note that an external 5V power supply is required when using several sensors and actuators. This is especially true if you use an LED light or a water pump.
![Wiring Diagram](./documentation/diagrams/wiring&#32;diagram/CIT-GardeningAdventure_bb.png)

## Docker Sensor Images

Each sensor has its own docker image. We use [Balenalib Raspbian](https://hub.docker.com/r/balenalib/rpi-raspbian) images which is optimized for the use in IoT devices. Use the -f option in the scripts directory to make sure Docker finds all the files it needs.
Example to build the dht sensor:

       .../gardening-adventure/scripts$ docker build -f dht_sensor/Dockerfile -t dht .

### Camera Configuration Options

The Raspberry Pi Camera module supports a variety of resolutions, ISO settings, Interval between Capture of Photos. All of these parameters are configurable. The camera_module.yml file takes all these parameters and deploys the camera module with the parameters requested. In the `spec` section, under `container` section, the options for the camera can be set under `arguments` section.

If no options under this section is set in the camera_module.yml file, the camera module is deployed with the default values. The default values and the supported values are described in the table below.

| Argument   | Description                         | Supported Values                                             | Default Value                       |
| ---------- | ----------------------------------- | ------------------------------------------------------------ | ----------------------------------- |
| resolution | Image resolution                    | 1920-1080, 3280-2464, 1640-1232, 1640-922, 1280-720, 640-480 | 1920-1080                           |
| output     | Location to store output.           | Any valid *nix path                                          | /camera_output/continuous_captures/ |
| interval   | Number of seconds between captures. | Must be an Integer.                                          | 10                                  |
| iso        | ISO Sensitivity Settings            | 100 - 800                                                    | 100                                 |

![Camera Configuration](./documentation/diagrams/camera-yml.png)

### Start Sensor and Actuators

If all required sensors are wired you can continue with the software installation. The installation of the desired devices is happening via a shell script. For that it is required that K3s is running on the Pi controlling the sensors and the IP address for the MQTT Broker is known.
To start the Sensors run the  ```gardening-adventure/scripts/sensor_deployment.sh``` script in an environment with [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/#verifying-kubectl-configuration) configured. After the deployment the sensors immediately start sending data to the MQTT Broker
**Note:** if you use your own Docker image reposetory please change this in the yml files.
# Reference

1. B.A.T.M.A.N installation and setup - [link](https://medium.com/@tdoll/how-to-setup-a-raspberry-pi-ad-hoc-network-using-batman-adv-on-raspbian-stretch-lite-dce6eb896687)
2. Raspbian image creation - [link](https://github.com/jonesinator/raspbian-remaster)
3. Dhcp configuration - [link](https://www.howtoforge.com/tutorial/install-and-configure-isc-dhcp-server-in-debian-9/)
