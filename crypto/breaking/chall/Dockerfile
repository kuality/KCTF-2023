FROM python:3.12-alpine

RUN apk add socat

WORKDIR /app

ENV PORT 11111

COPY chall.py .
COPY secret.py .

CMD socat -T60 -dd -v -v TCP-LISTEN:11111,reuseaddr,fork EXEC:"python3 chall.py",pty,stderr,setsid,sigint,sane
#CMD "socat", "-T60" , "-dd" , "-v" , "-v" , "TCP-LISTEN:"+$PORT+",reuseaddr,fork" , "EXEC:python3 chall.py", ",pty,stderr,setsid,sigint,sane"]