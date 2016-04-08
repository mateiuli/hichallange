FROM python:2.7
COPY requirements.txt /usr/src/hichallange/
WORKDIR /usr/src/hichallange
RUN pip install -r requirements.txt
