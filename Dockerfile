FROM python:3.6-alpine
ADD . /code
WORKDIR /code
RUN pip install --upgrade pip
RUN apk add build-base
RUN apk add postgresql-dev
RUN pip install -r requirements.txt
CMD ["python", "app/app.py"]
