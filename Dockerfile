# pull official base image
FROM python:3.8-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /usr/src

# python stuff
COPY ./requirements.txt .

RUN set -eux && \
    pip install --upgrade pip setuptools wheel && \ 
    pip install -r ./requirements.txt && \
    rm -rf /root/.cache/pip

# copy project source
COPY ./src .

ENTRYPOINT ["bash", "entrypoint.sh"]
