FROM python:alpine

ADD waterlevel.py /
ADD mqtt_client.py /

RUN pip install paho-mqtt


ENTRYPOINT ["python", "./waterlevel.py"]
