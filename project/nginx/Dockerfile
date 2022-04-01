FROM nginx:alpine

RUN apk update && apk add fail2ban

COPY certs /etc/certs

COPY ./entrypoint.sh /entrypoint.sh

ENTRYPOINT [ "/bin/sh", "/entrypoint.sh" ]