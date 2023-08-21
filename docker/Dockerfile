FROM ubuntu:20.04

ENV TZ=America/Toronto
LABEL authors="amanl@secureailabs.com"
USER root

# Set time zone data
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install dependencies
RUN apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y \
  wget \
  curl \
  sudo \
  git \
  build-essential \
  python3-pip \
  jq \
  unzip \
  cifs-utils \
  zip

COPY docker/requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# COPY docker/decrypt_file.py /decrypt_file.py
COPY docker/Entrypoint.sh /Entrypoint.sh

RUN chmod +x /Entrypoint.sh

COPY app /app
COPY sail_data_layer /sail_data_layer

ENTRYPOINT [ "/Entrypoint.sh" ]
