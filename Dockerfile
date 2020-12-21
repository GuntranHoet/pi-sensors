# set base image (host OS)
FROM python:3

LABEL maintainer="GunTheHuman"
LABEL build_version="0.2"

ENV BROKER=localhost
ENV USERNAME=""
ENV PASSWORD=""
ENV QOS=0

ENV CPU_TEMP_TOPIC="pi/cpu/temperature"
ENV CPU_USE_TOPIC="pi/cpu/use"

ENV MEM_TOTAL_TOPIC="pi/mem/total"
ENV MEM_FREE_TOPIC="pi/mem/free"
ENV MEM_USE_TOPIC="pi/mem/use"
ENV MEM_PERCENT_TOPIC="pi/mem/percent"

# set the working directory in the container
WORKDIR /usr/docker/pi-sensors

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY src/ .

# command to run on container start
CMD ["python", "-u", "./main.py"]
