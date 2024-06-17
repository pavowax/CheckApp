FROM python:latest

# Path: /app
WORKDIR /app

COPY . .

WORKDIR /app/checkApp

RUN pip install -r requirements.txt

EXPOSE 6700

CMD ["python", "main.py"]