FROM node:9.6.1
RUN mkdir /usr/src/app
WORKDIR /usr/src/app

RUN apt-get update && apt-get install vim -y
# add `/usr/src/app/node_modules/.bin` to $PATH
ENV PATH /usr/src/app/node_modules/.bin:$PATH

# install and cache app dependencies
COPY package.json /usr/src/app/package.json
RUN npm install
RUN npm install @angular/cli@1.7.1

COPY . /usr/src/app

# start app
CMD ng serve --host 0.0.0.0 --disableHostCheck true
EXPOSE 4200
