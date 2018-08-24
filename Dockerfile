FROM debian:latest

RUN apt-get update && apt-get install python3-pip libmariadbclient-dev -y
RUN pip3 install discord.py sqlalchemy mysqlclient nltk
RUN apt-get clean
RUN python3 -c 'import nltk; nltk.download("punkt")'

ADD . /vipper
WORKDIR /vipper

CMD python3 vipper2.py
