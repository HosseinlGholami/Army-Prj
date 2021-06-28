FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN apt-get update ##[edited]
RUN apt-get install ffmpeg libsm6 libxext6  -y

CMD [ "python3", "Sender.py"]