FROM python:3.11

RUN pip install --upgrade pip setuptools

RUN apt update

RUN useradd -rms /bin/bash bro && chmod 777 /opt /run

WORKDIR /watcher

ENV PYTHONPATH="${PYTHONPATH}:/watcher"

COPY --chown=bro:watcher . .

RUN pip install -r req.txt

USER bro