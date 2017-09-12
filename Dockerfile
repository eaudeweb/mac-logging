FROM python:2-alpine3.6
MAINTAINER "Cătălin Jitea <catalin.jitea@eaudeweb.ro"

ENV WORK_DIR=/var/local/pontaj
RUN runDeps="sqlite sqlite-dev" \
    && apk add --no-cache $runDeps \
    && mkdir -p $WORK_DIR/files

COPY requirements.txt $WORK_DIR/
WORKDIR $WORK_DIR
RUN pip install -r requirements.txt

COPY . $WORK_DIR/
ENTRYPOINT ["./docker-entrypoint.sh"]
