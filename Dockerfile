FROM python:3.7-stretch

WORKDIR /usr/src/app

RUN apt-get update

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --force-reinstall --ignore-installed -r requirements.txt
COPY app ./app
COPY coronavirus-tracker-api-swagger.yaml ./
COPY uwsgi.ini ./
COPY main.py ./

EXPOSE 5000

CMD ["uwsgi", "uwsgi.ini"]
