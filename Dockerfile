FROM python:3.10.4

WORKDIR /Aspid

COPY . .

RUN apt-get update
RUN pip install -r requirements.txt

VOLUME /Data

CMD [ "python3", "__main__.py" ]