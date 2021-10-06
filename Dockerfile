FROM python:3.8-slim-buster
WORKDIR /eetc-vault
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
ENV FLASK_APP=google_sheets_api.py
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
