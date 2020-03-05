#!/bin/bash
mosquitto=$("garden")

1>&2 echo "Install mosquitto..."
#helm install garden -f mosquitto.yaml --set nodeSelector.mqtt=mosquitto smizy/mosquitto
ready=$(kubectl get pods -l app=$mosquitto-mosquitto -o jsonpath='{.items..status.containerStatuses..ready}')
# check if mosquitto is ready
1>&2 echo "$ready"
while [ "$ready" != "true" ]; 
do
    ready=$(kubectl get pods -l app=$mosquitto-mosquitto -o jsonpath='{.items..status.containerStatuses..ready}')
    sleep 5
done
#start Nodeport for mosquitto
kubectl delete
1>&2 echo "$ready"

