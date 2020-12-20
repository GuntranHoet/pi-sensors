# set base image (host OS)
FROM python:3

LABEL maintainer="GunTheHuman"
LABEL build_version="0.1"

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
