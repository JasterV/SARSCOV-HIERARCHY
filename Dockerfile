FROM python:3.8
MAINTAINER manudiv1
WORKDIR /app
COPY ./src /app
COPY ./resources /app
COPY ./requeriments.txt /app
RUN apt-get update && apt-get install -y
RUN pip3 install -r requeriments.txt
CMD ["python","./main/sarscovhierarchy.py","."]