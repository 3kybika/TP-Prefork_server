FROM python:3

ADD ./httptest /var/www/html/httptest/

ENV WORK /opt
ADD ./ $WORK
WORKDIR $WORK

EXPOSE 80
CMD python3 main.py
