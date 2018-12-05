FROM jupyter/scipy-notebook
USER root
 RUN apt-get update && apt-get install vim -y 
 RUN conda install -c conda-forge cartopy netcdf4 gdal metpy
 RUN pip install flask flask-cors colour uwsgi psycopg2
 WORKDIR /scripts
 CMD ./uwsgi.sh
EXPOSE 5000

