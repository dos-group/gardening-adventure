FROM balenalib/apalis-imx6q-node

RUN apt-get update && apt-get install -y iptables batctl git

RUN git clone git@github.com:citlab/gardening-adventure.git
RUN cp gardening-adventure/batman/node/configs/* etc/network/interfaces.d/

RUN chmod 700 gardening-adventure/batman/node/garden-mesh.sh