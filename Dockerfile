FROM python:latest

# Path: /app
WORKDIR /app

COPY . .

WORKDIR /app/fenrir

RUN pip install -r requirements.txt

EXPOSE 6700

CMD ["python", "main.py"]