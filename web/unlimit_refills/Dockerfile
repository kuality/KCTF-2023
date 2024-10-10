FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

RUN apt update
RUN apt install apache2 php -y

WORKDIR /var/www/html/

RUN rm -rf index.html

COPY ./app /var/www/html/

CMD ["/usr/sbin/apachectl", "-DFOREGROUND"]
