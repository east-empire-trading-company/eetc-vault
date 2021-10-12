FROM python:3.8-slim-buster
WORKDIR /eetc-vault
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
ENV FLASK_APP=main.py
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 60 main:app
