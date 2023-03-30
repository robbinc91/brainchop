# syntax=docker/dockerfile:1

FROM python:3.9.16-alpine3.17

WORKDIR /brainchop

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
	pip install git+https://www.github.com/keras-team/keras-contrib.git && \
	pip install torch==1.13.1+cu117 torchvision==0.14.1+cu117 torchaudio==0.13.1 --extra-index-url https://download.pytorch.org/whl/cu117

COPY . .

ENV FLASK_APP=server.py

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]