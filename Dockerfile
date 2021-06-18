FROM python:3.8

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /backend

WORKDIR /backend

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
