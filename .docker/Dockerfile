FROM python:3.8 AS BUILD

COPY . .
COPY requirements.txt .

RUN python -m pip install -r requirements.txt

EXPOSE 5000
ENTRYPOINT ["python", "main.py"]