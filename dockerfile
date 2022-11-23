FROM python:alpine

WORKDIR /project
COPY . /project
RUN pip install flask requests gunicorn datetime

EXPOSE 5000

CMD gunicorn --bind 0.0.0.0:5000 wsgi:app

