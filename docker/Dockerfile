FROM ubuntu:bionic

WORKDIR /app

RUN \
  echo "Updating apt sources." && \
  apt-get -qq update && \
  echo "Installing required packages." && \
  apt-get -qq install \
  python3.6-dev \
  python3-pip \
  postgresql-client \
  postgresql-common \
  iputils-ping \
  curl

# Install Python packages
COPY app/requirements.txt .
RUN \
  echo "Installing python packages..." && \
  pip3 install -r requirements.txt

# Mount the codebase
ADD app /app

ARG DJANGO_SETTINGS_MODULE=photos.settings.prod
ARG DJANGO_SECRET_KEY=not-a-secret
RUN mkdir -p /static/ && ./manage.py collectstatic --noinput
