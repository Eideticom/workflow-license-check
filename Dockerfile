FROM python:3.8

RUN apt-get update

RUN apt-get install -y bzip2 xz-utils zlib1g libxml2-dev libxslt1-dev python3-pip

RUN pip install --upgrade pip setuptools wheel

RUN pip install scancode-toolkit==32.0.7

COPY spdx_review.py /spdx_review.py

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
