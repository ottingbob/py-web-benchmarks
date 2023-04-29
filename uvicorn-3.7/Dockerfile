FROM python:3.7.7-slim-buster

WORKDIR /app

RUN pip install --no-cache fastapi uvicorn

COPY main.py .

EXPOSE 7331

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "7331"]
