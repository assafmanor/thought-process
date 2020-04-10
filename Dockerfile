FROM ubuntu:latest
COPY requirements.txt /usr/src/thoughtprocess/requirements.txt
RUN apt-get update \
  && apt-get install -y python3.8 python3-pip\
  && python3.8 -m pip install --upgrade pip setuptools wheel \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3.8 python
RUN pip install -r /usr/src/thoughtprocess/requirements.txt
