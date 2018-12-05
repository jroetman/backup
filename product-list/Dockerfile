FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install vim -y
ADD . /code/
CMD tail -F anything
#python3 manage.py runserver 0.0.0.0:8000
EXPOSE 8000

