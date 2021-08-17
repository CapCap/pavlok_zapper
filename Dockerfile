FROM python:3.9.6-alpine3.14

RUN pip install pytz requests

COPY *.py .

 CMD ["python", "main.py"]