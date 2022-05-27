FROM python:3.9-alpine

WORKDIR /code

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
CMD ["python3", "redis_loader.py"]
