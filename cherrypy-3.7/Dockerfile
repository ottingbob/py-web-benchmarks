FROM python:3.7.7-slim-buster

WORKDIR /app

RUN mkdir app && \
  pip install --no-cache bottle cherrypy wsgi-request-logger cheroot


COPY server-aio.py ./
COPY ./app app/

ENV PYTHONUNBUFFERED 1
EXPOSE 7331

CMD [ "python", "server-aio.py" ]
