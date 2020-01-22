FROM resin/raspberrypi3-alpine:edge AS build
# Copy necessary files
ADD ldr_script.py /
ADD mqtt_client.py /
# Install build requirements
RUN apk add --no-cache \
      python3 gcc libc-dev parted-dev python3-dev
RUN pip3 install --upgrade pip

RUN pip3 install gpiozero
RUN pip3 install RPi.GPIO
RUN pip3 install paho-mqtt

ENTRYPOINT ["python3", "-u", "ldr_script.py"]
