FROM python:3.8-slim

COPY ./requirements.txt /
COPY ./init.sh /137f7aa2edeb6d9ef2b3d746925bab95df1d300730250bcf429859cfb6ffc28f.sh

RUN pip3 install -r /requirements.txt

ENTRYPOINT ["/137f7aa2edeb6d9ef2b3d746925bab95df1d300730250bcf429859cfb6ffc28f.sh"]
