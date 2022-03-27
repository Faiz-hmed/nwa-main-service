FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk add jpeg-dev zlib-dev libjpeg \
    && pip install Pillow \
    && apk del build-deps

RUN apk add --upgrade bash
RUN pip install -r requirements.txt


RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN adduser -D user

COPY . .
COPY frontend /vol/web/static/
# RUN rm -rf /vol/web/static
# RUN cp -rf /app/frontend/* /vol/web/static
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web/

USER user
EXPOSE 8000