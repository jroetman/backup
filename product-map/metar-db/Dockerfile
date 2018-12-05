FROM fernandoe/docker-python:0.0.4
RUN apt-get update && apt-get upgrade -y && apt-get -y python-dev libpq-dev python-lxml libxml12-dev libxslt1-dev zlib1g-dev binutils libproj-dev gdal-bin libcairo2-dev pango1.0-tests autoremove autoclean clean
RUN pip install pip setuptools -U
RUN pip install amqp 
RUN pip install anyjson


