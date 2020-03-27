#!/bin/bash
mosquitto="garden-mosquitto"
influxDB="garden-influxdb"
grafana="grafana-garden"
telegraf="telegraf-garden"

1>&2 echo "Install Mosquitto..."
helm install garden -f mosquitto.yaml smizy/mosquitto
ready=$(kubectl get pods -l app=$mosquitto -o jsonpath='{.items..status.containerStatuses..ready}')
# check if mosquitto is ready
1>&2 echo "Get Infos..."
while [ "$ready" != "true" ]; 
do
    ready=$(kubectl get pods -l app=$mosquitto -o jsonpath='{.items..status.containerStatuses..ready}')
    sleep 5
done

#get Pod name
mosquittoPod=$(kubectl get pods -l app=$mosquitto -o jsonpath='{.items..metadata.name}')

#start Nodeport for mosquitto
kubectl delete svc $mosquitto
kubectl expose pod $mosquittoPod --port=1883 --target-port=1883

export mosquittoIP=$(kubectl get svc -l  app=$mosquitto -o jsonpath='{.items..spec.clusterIP}')
1>&2 echo "----------INFO----------"
1>&2 echo "mosquitto installed"
1>&2 echo "Pod name = $mosquittoPod"
1>&2 echo "Broker IP = $mosquittoIP"
1>&2 echo ""

1>&2 echo $"Install InfluxDB..."
helm install $influxDB -f influxdb.yaml stable/influxdb
export influxdbIP=$(kubectl get svc -l app=$influxDB -o jsonpath='{.items..spec.clusterIP}')
1>&2 echo "----------INFO----------"
1>&2 echo "InfluxDB installed"
1>&2 echo "InfluxDB IP: $influxdbIP"
1>&2 echo "Default username: admin"
1>&2 echo "Default Password: dspj2020"
1>&2 echo ""

1>&2 echo "Install Grafana..."
helm install $grafana -f grafana.yaml stable/grafana
export grafanaIP=$(kubectl get svc -l release=$grafana -o jsonpath='{.items..spec.clusterIP}')
1>&2 echo "----------INFO----------"
1>&2 echo "Grafana installed"
1>&2 echo "Grafana IP: $grafanaIP"
1>&2 echo "Default username: admin"
1>&2 echo "Default Password: dspj2020"
1>&2 echo ""

>&2 echo "Install Telegraf..."
source /dev/stdin <<<"$(echo 'cat <<EOF >final.yaml'; cat telegraf.yaml; echo EOF;)"
1>&2 echo "----------INFO----------"
1>&2 echo "Telegraf installed"
1>&2 echo ""
helm install $telegraf -f final.yaml stable/telegraf
rm final.yaml


