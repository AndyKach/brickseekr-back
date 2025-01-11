FROM python:3.12
ENV TZ=Europe/Berlin

RUN apt-get -y update \
 && apt-get -y upgrade

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY /src /src
WORKDIR /src

CMD ["uvicorn", "main:app", "--reload", "--port", "8000", "--host", "localhost"]
