FROM python:3.7-slim
RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y update && apt-get install -y --no-install-recommends \
		python3-pip python3-dev python3-setuptools gcc netcat tk supervisor
RUN rm -rf /var/lib/apt/lists/*
RUN apt-get -y autoremove
RUN apt-get -y clean
RUN apt-get -y autoclean
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt
RUN pip install gunicorn
