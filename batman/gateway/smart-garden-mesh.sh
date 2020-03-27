sudo batctl if add wlan0

sudo batctl gw_mode server

sudo ifconfig wlan0 up
sudo ifconfig bat0 up

sudo service isc-dhcp-server start
sudo systemctl enable isc-dhcp-server

sudo systemctl daemon-reload
sudo systemctl enable port-forwarding.service
sudo systemctl start port-forwarding.service
