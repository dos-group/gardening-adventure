sudo batctl if add wlan0

sudo batctl gw_mode server

sudo sysctl -w net.ipv4.ip_forward=1
sudo iptables -t nat -A POSTROUTING -o enxb827ebb206b4 -j MASQUERADE
sudo iptables -A FORWARD -i enxb827ebb206b4 -o bat0 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i bat0 -o enxb827ebb206b4 -j ACCEPT

sudo ifconfig wlan0 up
sudo ifconfig bat0 up
