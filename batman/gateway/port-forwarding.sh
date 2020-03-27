#!/bin/bash -

sudo sysctl -w net.ipv4.ip_forward=1
ETH=`ip link | awk -F: '$0 !~ "lo|vir|wl|^[^0-9]"{print $2a;getline}' | head -n 1`
sudo iptables -t nat -A POSTROUTING -o $ETH -j MASQUERADE
sudo iptables -A FORWARD -i $ETH -o bat0 -j ACCEPT
sudo iptables -A FORWARD -i bat0 -o $ETH -j ACCEPT