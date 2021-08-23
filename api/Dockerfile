# start from base
FROM python:3.7-alpine

WORKDIR /app

ENV ACCESS_KEY=.
ENV SECRET_ACCESS_KEY=.

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "./api.py" ]