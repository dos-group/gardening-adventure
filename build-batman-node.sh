#!/bin/bash -e
# This script is an example script showing how a full Raspbian image can be
# built and customized end-to-end. This script adds just a few things to the
# minimal install built by the build-raspbian script. It brings up the ethernet
# port with DHCP, allows domain names to be resolved, and installs a text
# editor. It is expected that the end-user of this library will modify this
# script to create custom images. It is even possible to make multiple images
# by calling the build-image script multiple times with different image names
# after re-customizing. That could be useful for creating a cluster of
# raspberry pis each with hardcoded static IPs.
if [[ $# -eq 0 ]] ; then
    echo "usage: ./build-batman-node -t [type] -n [hostname] -u [k3s_url] -k [k3s_token]"
    exit
fi

while [[ "$#" -gt 0 ]]
do
    case $1 in 
        -h|--help)
        echo "usage: ./build-batman-node -t [type] -n [hostname] -u [k3s_url] -k [k3s_token]"
        exit;;
        -t)
        TYPE="$2"
        ;;
        -n)
        HOSTNAME="$2"
        ;;
        -u)
        K3S_URL="$2"
        ;;
        -k)
        K3S_TOKEN="$2"
        ;;
    esac
shift
done

CHROOT="${RASPBIAN_REMASTER_CHROOT:-./raspbian}"
IMAGE="${RASPBIAN_REMASTER_IMAGE:-./images/raspbian.img}"
"$(dirname "${BASH_SOURCE[0]}")"/build-raspbian "${CHROOT}"

chroot "${CHROOT}" apt-get install -y dhcpcd5 openresolv vim batctl iptables wireless-tools sudo curl ssh

# # Set eth0 to use DHCP.
cat << EOF > "${CHROOT}/etc/network/interfaces.d/eth0"
allow-hotplug eth0
iface eth0 inet dhcp
EOF

case $TYPE in
    gateway)
        # Install dhcp server
        chroot "${CHROOT}" apt-get install -y isc-dhcp-server

        # Set network configurations for BATMAN
        cat .batman/gateway/wlan0 > "${CHROOT}/etc/network/interfaces.d/wlan0"
        cat .batman/gateway/bat0 > "${CHROOT}/etc/network/interfaces.d/bat0"

        # Set DHCP Server Configuration
        cat .batman/gateway/dhcpd.conf > "${CHROOT}/etc/dhcp/dhcpd.conf"
        cat .batman/gateway/isc-dhcp-server > "${CHROOT}/etc/default/isc-dhcp-server"

        # Add configuration script
        cat .batman/gateway/smart-garden-mesh.sh > "${CHROOT}/root/smart-garden-mesh.sh"
        cat .batman/gateway/port-forwarding.sh > "${CHROOT}/root/port-forwarding.sh"
        chroot "${CHROOT}" /bin/bash -c "chmod +755 /root/port-forwarding.sh"
        cat ./gateway/port-forwarding.service > "${CHROOT}/etc/systemd/system/port-forwarding.service";;
    node)
        # Set network configurations for BATMAN
        cat .batman/node/wlan0 > "${CHROOT}/etc/network/interfaces.d/wlan0"
        cat .batman/node/bat0 > "${CHROOT}/etc/network/interfaces.d/bat0"

        # Add configuration script
        cat .batman/node/smart-garden-mesh.sh > "${CHROOT}/root/smart-garden-mesh.sh";; 
    *)
esac

# # Deny dhcp for wlan interface
echo "denyinterfaces wlan0" >> "${CHROOT}/etc/dhcpcd.conf"

# # Set Hostname
sed -i "1 i\127.0.0.1       ${HOSTNAME}" "${CHROOT}/etc/hosts"
sed -i "1s/.*/${HOSTNAME}/" "${CHROOT}/etc/hostname"

# # Start BATMAN automatically on boot
echo "batman-adv" >> "${CHROOT}/etc/modules"

# # Add script for k3s installation
echo "curl -sfL https://get.k3s.io | K3S_URL=${K3S_URL} K3S_TOKEN=${K3S_TOKEN} sh -" > "${CHROOT}/root/k3s_installation.sh"

chroot "${CHROOT}" /bin/bash -c "chmod +755 /root/smart-garden-mesh.sh"
chroot "${CHROOT}" /bin/bash -c "chmod +755 /root/k3s_installation.sh"
# # Set the root password. This is obviously not secure. Real customization
# # scripts should override this, or use 
chroot "${CHROOT}" /bin/bash -c "echo \"root:raspberry\" | chpasswd"

# # Adding drivers for wifi
mkdir -p "${CHROOT}/lib/firmware/brcm"
cp -R brcm/* "${CHROOT}/lib/firmware/brcm/"

"$(dirname "${BASH_SOURCE[0]}")"/build-image "${CHROOT}" "${IMAGE}"
