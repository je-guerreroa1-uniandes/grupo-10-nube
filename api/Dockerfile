# Este no sirve con estas depencencias
# FROM python:3.12.0a7-slim-bullseye 
FROM python:3.9.16-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

# ENV FLASK_APP=flaskr/app.py
CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]