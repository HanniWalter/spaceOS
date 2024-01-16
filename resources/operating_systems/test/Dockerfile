FROM ubuntu:22.04

####

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3\
    python3-pip 

RUN pip3 install toml

RUN mkdir /control
WORKDIR /control
COPY . .

####