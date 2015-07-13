FROM azukiapp/deploy
MAINTAINER Azuki <support@azukiapp.com>

WORKDIR /azk/deploy
COPY deploy-do.sh ./deploy-do.sh
COPY setup.py ./setup.py

RUN apt-get -y update \
  && apt-get install -y python-dev libffi-dev libssl-dev \
  && pip install -U ndg-httpsclient \
  && pip install -U python-digitalocean

ENTRYPOINT ["/azk/deploy/deploy-do.sh"]
