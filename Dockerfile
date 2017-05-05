FROM python:3.6

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    python-pip

COPY requirements.txt /tmp/

# for running matplotlib correctly in docker
ENV MPLBACKEND="agg"

RUN pip install -r /tmp/requirements.txt

COPY . /opt/corners

WORKDIR /opt/corners

CMD bash