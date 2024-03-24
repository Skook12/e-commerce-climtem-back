FROM python:3.8 AS BUILD

WORKDIR /app
COPY . /app
COPY requirements.txt /app

RUN python -m pip install -r requirements.txt

EXPOSE 5000
ENTRYPOINT ["python", "main.py"]