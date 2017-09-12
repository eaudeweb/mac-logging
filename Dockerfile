FROM python:2.7-slim

ENV WORK_DIR=/var/local/mac-logging

RUN runDeps="curl vim build-essential sqlite3 libsqlite3-dev" \
 && apt-get update \
 && apt-get install -y --no-install-recommends $runDeps \
 && rm -vrf /var/lib/apt/lists/*

COPY requirements.txt $WORK_DIR/
WORKDIR $WORK_DIR
RUN pip install -r requirements.txt

COPY . $WORK_DIR/
RUN mv docker-entrypoint.sh /bin/

ENTRYPOINT ["docker-entrypoint.sh"]
