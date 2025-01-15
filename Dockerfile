FROM python:3.9-slim-buster

RUN apt-get -y update
RUN apt-get -y install --reinstall build-essential
RUN apt-get -y install swig
RUN apt-get -y install gcc

User root
WORKDIR /app

RUN pip3 install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# Run app on port default 5000
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]