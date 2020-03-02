# Restart the interface configuration
sudo ip addr flush bat0
sudo ifconfig bat0 down
sudo ifconfig wlan0 down
sudo /etc/init.d/networking restart

sudo batctl if add wlan0

sudo ifconfig wlan0 up
sudo ifconfig bat0 up
