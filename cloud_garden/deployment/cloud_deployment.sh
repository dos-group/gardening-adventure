#!/bin/bash
mosquitto="garden"
influxDB="garden-influxdb"
grafana="grafana-garden"
telegraf="telegraf-garden"

1>&2 echo "Install Mosquitto..."
helm install garden -f mosquitto.yaml --set nodeSelector.mqtt=mosquitto smizy/mosquitto
ready=$(kubectl get pods -l app=$mosquitto-mosquitto -o jsonpath='{.items..status.containerStatuses..ready}')
# check if mosquitto is ready
1>&2 echo "Get Infos..."
while [ "$ready" != "true" ]; 
do
    ready=$(kubectl get pods -l app=$mosquitto-mosquitto -o jsonpath='{.items..status.containerStatuses..ready}')
    sleep 5
done

#get Pod name
mosquittoPod=$(kubectl get pods -l app=$mosquitto-mosquitto -o jsonpath='{.items..metadata.name}')

#start Nodeport for mosquitto
kubectl delete svc $mosquitto-mosquitto
kubectl expose pod $mosquittoPod --port=1883 --target-port=1883

export mosquittoIP=$(kubectl get svc -l  app=garden-mosquitto -o jsonpath='{.items..spec.clusterIP}')

1>&2 echo "mosquitto installed"
1>&2 echo "POD = $mosquittoPod"
1>&2 echo "IP = $mosquittoIP"
1>&2 echo ""

1>&2 echo $"Install InfluxDB..."
helm install $influxDB -f influxdb.yaml --set nodeSelector.databases=influxdb stable/influxdb

export influxdbIP=$(kubectl get svc -l app=$influxDB -o jsonpath='{.items..spec.clusterIP}')
1>&2 echo ""

1>&2 echo "Install Grafana..."
helm install $grafana -f grafana.yaml stable/grafana
1>&2 echo ""

>&2 echo "Install Telegraf..."
source /dev/stdin <<<"$(echo 'cat <<EOF >final.yaml'; cat telegraf.yaml; echo EOF;)"

helm install $telegraf -f final.yaml stable/telegraf
rm final.yamlf


