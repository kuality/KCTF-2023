FROM ubuntu:22.04

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y xinetd
RUN apt-get update && apt-get install -y netcat
ENV TERM=linux


RUN useradd -m ctf
WORKDIR /home/ctf

ADD nc /home/ctf
ADD ctf /etc/xinetd.d

COPY flag.txt /home/ctf/

RUN chmod 460 /home/ctf/*
RUN chown ctf:root /home/ctf/*
RUN chmod +x /home/ctf/nc

RUN echo "ctf 10019/tcp" >> /etc/services

CMD ["/usr/sbin/xinetd", "-dontfork"]

