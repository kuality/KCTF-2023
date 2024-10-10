FROM ubuntu:20.04

RUN apt update

RUN apt install python3 python3-pip -y

RUN python3 -m pip install flask

RUN useradd --password=kctf -m kctf

COPY ./app /home/kctf/app

WORKDIR /home/kctf/app/

USER kctf

ENTRYPOINT ["python3", "app.py"]
