FROM python:3.7
 RUN apt-get install git -y
COPY . /app/
 CMD /bin/bash
