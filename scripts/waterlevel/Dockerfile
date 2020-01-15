FROM python:3.9.0a2-alpine3.10

ADD waterlevel.py
ADD ../mqtt_client.py

RUN pip install paho-mqtt


ENTRYPOINT ["python waterlevel.py"]
