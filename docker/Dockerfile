FROM node:12 as frontend

WORKDIR /frontend

# Install Node modules, build Webpack for prod.
COPY frontend/package.json .
COPY frontend/yarn.lock .
RUN echo "Installing Node modules." && \
  yarn install

# Mount the codebase
ADD frontend /frontend

# Build webpack from production
RUN echo "Building Webpack." && \ 
  yarn build


# Main container
FROM ubuntu:bionic

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND noninteractive
ENV TIMEZONE Australia/Melbourne

# Copy frontend assets
COPY --from=frontend /build /build

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
