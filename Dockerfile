FROM ubuntu:latest

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


RUN \
  echo "Installing remote_syslog2 for Papertrail" && \
  curl \
    --location \
    --silent \
    https://github.com/papertrail/remote_syslog2/releases/download/v0.20/remote-syslog2_0.20_amd64.deb \
    -o /tmp/remote_syslog.deb && \
  dpkg -i /tmp/remote_syslog.deb


# Install Python packages
COPY app/requirements.txt .
RUN \
	echo "Installing python packages..." && \
  pip3 install -r requirements.txt

# Mount the codebase
ADD app /app
