#!/bin/bash

node_exists() {
  node="$(kubectl get nodes $nodeName -o jsonpath='{.metadata.name}')"

  if [ -z "$node" ];
  then
        1>&2 echo "Node does not exists! Please enter existing node:"
        read nodeName
        node_exists
  fi
}

all_sensor () {
  ldr_sensor
  rgb_light
  dht_sensor
  moisture_sensor
  waterlevel_sensor
  camera_sensor
}

ldr_sensor () {
  1>&2 echo "Please enter label for the nodeselection"
  read nodeName
  node_exists

  1>&2 echo "Please enter name for the pod"
  read podName

  1>&2 echo "Please enter the mqtt broker IP"
  read brokerIP
  source /dev/stdin <<<"$(echo 'cat <<EOF >./ldr_sensor/final.yml'; cat ./ldr_sensor/ldr.yml; echo EOF;)"
  kubectl apply -f  ./ldr_sensor/final.yml
  rm ./ldr_sensor/final.yml
}

rgb_light () {
  1>&2 echo "Please enter node name for the nodeselection"
  read nodeName
  node_exists

  1>&2 echo "Please enter name for the pod"
  read podName

  1>&2 echo "Please enter the mqtt broker IP"
  read brokerIP
  source /dev/stdin <<<"$(echo 'cat <<EOF >./light/final.yml'; cat ./light/rgb_light.yml; echo EOF;)"
  kubectl apply -f  ./light/final.yml
  rm ./light/final.yml
}

dht_sensor () {
  1>&2 echo "Please enter node name for the nodeselection"
  read nodeName
  node_exists

  1>&2 echo "Please enter name for the pod"
  read podName

  1>&2 echo "Please enter the mqtt broker IP"
  read brokerIP
  source /dev/stdin <<<"$(echo 'cat <<EOF >./dht_sensor/final.yml'; cat ./dht_sensor/dht.yml; echo EOF;)"
  kubectl apply -f  ./dht_sensor/final.yml
  rm ./dht_sensor/final.yml
}

moisture_sensor () {
  1>&2 echo "Please enter node name for the nodeselection"
  read nodeName
  node_exists

  1>&2 echo "Please enter name for the pod"
  read podName

  1>&2 echo "Please enter the mqtt broker IP"
  read brokerIP
  source /dev/stdin <<<"$(echo 'cat <<EOF >./moisture_sensor/final.yml'; cat ./moisture_sensor/moisture.yml; echo EOF;)"
  kubectl apply -f  ./moisture_sensor/final.yml
  rm ./moisture_sensor/final.yml
}
waterlevel_sensor () {
  1>&2 echo "Please enter node name for the nodeselection"
  read nodeName
  node_exists

  1>&2 echo "Please enter name for the pod"
  read podName

  1>&2 echo "Please enter the mqtt broker IP"
  read brokerIP
  source /dev/stdin <<<"$(echo 'cat <<EOF >./waterlevel_sensor/final.yml'; cat ./waterlevel_sensor/waterlevel.yml; echo EOF;)"
  kubectl apply -f  ./waterlevel_sensor/final.yml
  rm ./waterlevel_sensor/final.yml
}

camera_sensor () {
  1>&2 echo "Please enter node name for the nodeselection"
  read nodeName
  node_exists

  1>&2 echo "Please enter name for the pod"
  read podName

  1>&2 echo "Please enter the mqtt broker IP"
  read brokerIP
  source /dev/stdin <<<"$(echo 'cat <<EOF >./camera_module/final.yml'; cat ./camera_module/camera_module.yml; echo EOF;)"
  kubectl apply -f  ./camera_module/final.yml
  rm ./camera_module/final.yml
}





case_func () {
  1>&2 echo "Deploy all devices: 0"
  1>&2 echo "Deploy ldr sensor: 1"
  1>&2 echo "Deploy light device: 2"
  1>&2 echo "Deploy dht sensor: 3"
  1>&2 echo "Deploy moisture sensor: 4"
  1>&2 echo "Deploy waterlevel sensor: 5"
  1>&2 echo "Deploy camera sensor: 6"

  read option
  case "$option" in
    0) 1>&2 echo "-0 deploy all devices " 
       all_sensor;; 
    1) 1>&2 echo "-1 deploy ldr sensor " 
       ldr_sensor;; 
    2) 1>&2 echo "-2 deploy the RGB light device " 
       rgb_light;; 
    3) 1>&2 echo "-3 deploy dht sensor " 
       dht_sensor;; 
    4) 1>&2 echo "-4 deploy moisture sensor " 
     moisture_sensor;; 
    5) 1>&2 echo "-5 deploy waterlevel sensor " 
       waterlevel_sensor;; 
    6) 1>&2 echo "-6 deploy camera sensor " 
       camera_sensor;; 
    *) 1>&2 echo "Option $option not recognized"
       1>&2 echo "" 
       case_func;;

  	esac
   
  	shift
  }
case_func



