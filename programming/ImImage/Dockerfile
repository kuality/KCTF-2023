FROM python:3.12-alpine

ADD server.py /app/server.py
ADD flag.bmp /app/flag.bmp
ADD requirements.txt /app/requirements.txt
WORKDIR /app/

RUN pip install -r requirements.txt

ENV HOST=0.0.0.0
ENV PORT=8080

EXPOSE 8080

ENTRYPOINT [ "python3", "server.py" ]