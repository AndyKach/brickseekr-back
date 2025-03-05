FROM python:3.12
ENV TZ=Europe/Berlin

RUN set +x \
 && apt update \
 && apt upgrade -y \
 && apt install -y curl gcc build-essential \
 && apt-get install -y firefox-esr


COPY requirements.txt .
RUN pip install -r requirements.txt

COPY /src /src
WORKDIR /src

RUN chmod +x geckodriver

CMD ["uvicorn", "main:app", "--reload", "--port", "8000", "--host", "localhost"]
