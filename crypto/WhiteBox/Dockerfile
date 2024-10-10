FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN pip install numpy 
RUN pip install pycryptodome 
RUN apt install -y sagemath 
RUN apt install socat -y

WORKDIR /app

ENV PORT 12322

COPY chall.py .
COPY flag.txt .

CMD socat -T60 -dd -v -v TCP-LISTEN:12322,reuseaddr,fork EXEC:"python3 chall.py",pty,stderr,setsid,sigint,sane,echo=0


