FROM python:3.8-buster

# set work directory
WORKDIR /app

# update
RUN apt update -y
RUN apt upgrade -y

# copy project
COPY . .

# add and run as not root user
RUN adduser -D test
USER test

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0


# install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# run gunicorn
CMD gunicorn -w 4 "manage:create_app()"

