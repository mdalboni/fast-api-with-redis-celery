# pull official base image
FROM python:3.11-slim-buster
RUN apt-get update && apt-get install -y make
# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip

# create the virtual environment for our python project
RUN python -m venv ./.venv

COPY ./*requirements.txt .
RUN pip install -r dev_requirements.txt

# copy project src
COPY ./src .

EXPOSE 8000