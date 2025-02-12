FROM python:3.12

WORKDIR /app
COPY .. /app
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
EXPOSE 8000