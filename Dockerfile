FROM ubuntu:latest

RUN mkdir -p /home/app

COPY . /home/app
WORKDIR "/home/app"

#RUN apt-get update
RUN apt-get -y update
RUN apt-get install python3 -y
RUN apt install -y python3-pip
RUN pip3 install Flask
RUN pip3 install Flask-Session
RUN pip3 install sqlalchemy
RUN pip3 install Flask-SQLAlchemy

EXPOSE 5000

ENTRYPOINT [ "python3" ]
CMD ["application.py"]