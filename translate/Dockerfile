FROM python
ENV PYTHONUNBUFFERED 1
RUN mkdir /translate
WORKDIR /translate
ADD requirements.txt /translate/
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
ADD . /translate/
