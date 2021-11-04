FROM ubuntu:latest

RUN mkdir -p /home/app
RUN apt-get -y update
RUN apt-get install python3 -y 
RUN apt install -y python3-pip

COPY . /home/app
WORKDIR "/home/app"

RUN apt install -y apparmor apturl
RUN pip3 install -r requirements.txt

EXPOSE 8080

CMD ["python3", "application.py"]