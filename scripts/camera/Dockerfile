FROM hypriot/wiringpi:latest

ADD camera_pi.py /

RUN apt update
RUN apt-get install python3
RUN apt-get install python3-pip
RUN apt-get install python3-dev

RUN pip3 install picamera

ENTRYPOINT ["python3", "-u", "/camera_pi.py"]
