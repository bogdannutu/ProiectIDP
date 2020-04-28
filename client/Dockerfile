FROM python:3.6

WORKDIR /client

COPY requirements.txt /client
RUN pip install -r requirements.txt

COPY client.py /client
CMD python client.py http://admin:5000/ http://service:5000/
