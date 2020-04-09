FROM python:3.7.7-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN mkdir app && \
  apt-get update && \
  apt-get install gcc libev-dev -y && \
  pip install --no-cache -r requirements.txt && \
  pip install --no-cache --no-binary :all: hug

COPY ./app app/

EXPOSE 7331

CMD ["python", "/app/app/main.py"]
