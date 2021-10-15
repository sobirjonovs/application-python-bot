FROM python:latest

RUN mkdir /src
WORKDIR /src
COPY requirements /src/
RUN pip install -r requirements
COPY . /src
RUN python main.py
