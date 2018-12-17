FROM ubuntu:bionic

WORKDIR /app

RUN \
	echo "Updating apt sources." && \
    apt-get -qq update && \
    echo "Installing required packages." && \
    apt-get -qq install \
        python3 \
        python3-setuptools \
        python3-dev \
       	python3-pip \
       	postgresql-client \
       	postgresql-common \
        curl \
        iputils-ping


# Install Papertrail
RUN \
  echo "Installing remote_syslog2 for Papertrail" && \
  curl \
    --location \
    --silent \
    https://github.com/papertrail/remote_syslog2/releases/download/v0.20/remote-syslog2_0.20_amd64.deb \
    -o /tmp/remote_syslog.deb && \
  dpkg -i /tmp/remote_syslog.deb


# Install NodeJS and Yarn
RUN \
  curl -sL https://deb.nodesource.com/setup_9.x | bash - && \
  apt-get -qq install nodejs build-essential
RUN \
  curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
  echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
RUN echo "Updating apt sources... again" && apt-get -qq update
RUN apt-get install yarn


# Install Python packages
COPY app/requirements.txt .
RUN \
	echo "Installing python packages..." && \
  pip3 install -r requirements.txt


# Install NPM packages
COPY app/package.json .
RUN yarn install


# Mount the codebase
ADD app /app


# Run frontend build
RUN yarn prod

ARG DJANGO_SETTINGS_MODULE=photos.settings.prod
ARG DJANGO_SECRET_KEY=not-a-secret
RUN mkdir -p /static/ && ./manage.py collectstatic --noinput
