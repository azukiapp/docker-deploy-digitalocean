FROM azukiapp/deploy
MAINTAINER Azuki <support@azukiapp.com>

WORKDIR /azk/deploy

RUN apt-get -y update \
  && apt-get install -y python-dev libffi-dev libssl-dev \
  && pip install -U ndg-httpsclient \
  && pip install -U python-digitalocean \
  && apt-get clean -qq \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY deploy-digitalocean.sh setup.py log.py ./

ENTRYPOINT ["/azk/deploy/deploy.sh", "--provider", "digitalocean"]
CMD [""]
