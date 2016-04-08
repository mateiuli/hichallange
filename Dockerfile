FROM python:2.7
COPY . /usr/src/hichallange
ADD hic_cron /etc/cron.d/
WORKDIR /usr/src/hichallange
RUN pip install -r requirements.txt
#RUN apt-get update && apt-get -y install cron
#RUN crontab /usr/src/hichallange/hic_cron
#RUN python WikiEvents.py
