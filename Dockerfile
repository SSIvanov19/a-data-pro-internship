FROM python:3.9-buster

# System deps:
ADD odbcinst.ini /etc/odbcinst.ini

RUN apt-get update && apt-get install gcc && apt-get install -y tdsodbc unixodbc-dev && apt install unixodbc-bin -y && apt-get clean -y && pip install poetry && mkdir -p app/src
# Copy only requirements to cache them in docker layer

ADD . /app/src
WORKDIR /app/src
# Project initialization:
RUN pip install -r requirements.txt 

# Run the app:
CMD ["python3","./app/manage.py", "runserver"]