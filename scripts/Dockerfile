FROM hypriot/wiringpi:latest

ADD waterlevel.py /
ADD mqtt_client.py /

RUN pip install RPi.GPIO
RUN pip install paho-mqtt
ENTRYPOINT ["python", "/waterlevel.py"]
