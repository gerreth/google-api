FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install --upgrade google-api-python-client

COPY . .

CMD [ "python", "./main.py" ]
