FROM python:3.11-slim-bullseye

RUN apt update && \
    apt install -y ffmpeg && \
    useradd -u 1000 1000 && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /root/.ssh/

WORKDIR /Aspid
ADD . .
RUN mkdir -p ./Aspid/Data

RUN pip install -r requirements.txt

USER 1000

CMD [ "python3", "__main__.py" ]
