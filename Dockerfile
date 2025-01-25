FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*
# RUN apt-get -y install --reinstall build-essential
# RUN apt-get -y install swig
# RUN apt-get -y install gcc

User root
WORKDIR /app

RUN pip3 install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

# Run app on port default 5000
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]