# syntax=docker/dockerfile:1

FROM tensorflow/tensorflow:2.5.0-gpu

WORKDIR /brainchop

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
	pip install git+https://www.github.com/keras-team/keras-contrib.git && \
	#pip install torch==1.13.1+cu117 torchvision==0.14.1+cu117 torchaudio==0.13.1 --extra-index-url https://download.pytorch.org/whl/cu117 &&\
	pip install git+https://github.com/lucasb-eyer/pydensecrf.git && \
	pip install --upgrade --pre SimpleITK --find-links https://github.com/SimpleITK/SimpleITK/releases/tag/latest

COPY . .

ENV FLASK_APP=server.py

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]