FROM python:3.7.7-slim-buster

WORKDIR /app

RUN mkdir app && \
  pip install --no-cache flask gunicorn

COPY entrypoint.sh start.sh gunicorn_conf.py ./
COPY ./app app/

RUN chmod +x entrypoint.sh start.sh

EXPOSE 7331

ENTRYPOINT [ "/app/entrypoint.sh" ]
CMD [ "/app/start.sh" ]
