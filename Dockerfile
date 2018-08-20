FROM debian:latest

RUN apt-get update && apt-get install python3-pip libmariadbclient-dev -y
RUN apt-get clean

RUN pip3 install discord.py sqlalchemy mysqlclient

ADD . /vipper
WORKDIR /vipper

CMD python3 vipper2.py
