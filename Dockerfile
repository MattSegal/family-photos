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
        curl

# Install Python packages
COPY app/requirements.txt .
RUN \
	echo "Installing python packages..." && \
    pip3 install -U pip && \
    pip3 install -r requirements.txt

# Mount the codebase
ADD app /app
