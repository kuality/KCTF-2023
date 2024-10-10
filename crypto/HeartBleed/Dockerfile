FROM python:3.10-alpine

RUN apk add socat

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir pycryptodome

WORKDIR /app

ENV HOST=0.0.0.0
ENV PORT=12321

EXPOSE 12321

COPY chall.py .
COPY flag.txt .
COPY memory.txt .

CMD socat -T60 -dd -v -v TCP-LISTEN:12321,reuseaddr,fork EXEC:"python3 chall.py",pty,stderr,setsid,sigint,sane,echo=0

