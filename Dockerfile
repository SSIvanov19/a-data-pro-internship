FROM python:3.9-buster

# System deps:
ADD odbcinst.ini /etc/odbcinst.ini

RUN apt-get update && apt-get install gcc && apt-get install -y tdsodbc unixodbc-dev && apt install unixodbc-bin -y && apt-get clean -y && pip install poetry && mkdir -p app/src
# Copy only requirements to cache them in docker layer

ADD . /app/src
WORKDIR /app/src
# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev

CMD ["python3","./crawler_files/crawler_files/startCrawling.py"]