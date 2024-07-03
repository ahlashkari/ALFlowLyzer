FROM ubuntu:20.04

# Disable Prompt During Packages Installation
ARG DEBIAN_FRONTEND=noninteractive
FROM python:3.8-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=0
ENV PYTHONPATH=/Project

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY . /Project/
WORKDIR /Project

RUN python setup.py install
ENTRYPOINT [ "/bin/bash" ]

RUN alflowlyzer
