FROM python:3.9.6-alpine3.14

COPY *.py .

 CMD ["python", "main.py"]